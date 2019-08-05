import boto3
import time
import random
import datetime

#-----------------------------#
# SPOT REQUEST SPECIFICATIONS #
#-----------------------------#

REGION = ''
client = boto3.client('ec2', region_name=REGION)

# -- Instance Description -- #
instance_name = ""
key_pairs = ""
instance_prefix = ['-A', '-B', '-C']
instance_type = ''
instance_description = 'Linux/UNIX'
ami_id = ''

# -- VPC Description -- #
number_of_subnets = 3
subnets_id_list = ["subnet-id", "subnet-id", "subnet-id"]
zones = ["zone-1a", "zone-1b", "zone-1c"]
security_group = 'sg-id'

# -- ELB Description -- #
target_group_arn = 'arn'

# -- Flags -- #
bool_values = [0] * number_of_subnets
name_tag_index = 0

# -- Current Spot Price Values -- #
year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day

#-----------------------------------#
# DETERMINE ZONE TO DEPLOY INSTANCE #
#-----------------------------------#

ec2 = boto3.resource('ec2', region_name=REGION)
for x in range(0,number_of_subnets):
    for i in ec2.instances.filter(
        Filters=[
            {
                'Name': 'availability-zone',
                'Values': [
                    zones[x]
                ]
            },
        ],
    ):
        if i.tags[name_tag_index]['Value'] == instance_name+instance_prefix[x] and i.state['Code'] == 16: 
            print(instance_name+instance_prefix[x] + " already exists!")
            bool_values[x] = 1

for j in range(0,number_of_subnets):
    if bool_values[j] == 0:
        print("Launching instance in zone" + instance_prefix[j])
        spot_subnet = subnets_id_list[j]
        instance_name = instance_name+instance_prefix[j]
        availability_zone = zones[j]
        break
    elif j == (number_of_subnets-1):
        random_zone = random.randint(0,number_of_subnets-1)
        print("Launching in random zone")
        print("Launching instance in zone" + instance_prefix[random_zone])
        spot_subnet = subnets_id_list[random_zone]
        instance_name = instance_name+instance_prefix[random_zone]
        availability_zone = zones[random_zone]

#---------------------------------#
# GET SPOT PRICE FOR SPOT REQUEST #
#---------------------------------#

response = client.describe_spot_price_history(
    EndTime=datetime.datetime(year, month, day),
    AvailabilityZone=availability_zone,
    InstanceTypes=[
        instance_type,
    ],
    ProductDescriptions=[
        instance_description,
    ],
    StartTime=datetime.datetime(year, month, day),
)

# -- Grab current spot price -- #
instance_spot_price = response['SpotPriceHistory'][0]['SpotPrice']

#-----------------------#
# REQUEST SPOT INSTANCE #
#-----------------------#

instance = client.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification={
        'ImageId': ami_id,
        'InstanceType': instance_type,
        'KeyName': key_pairs,
        'Monitoring': {
            'Enabled': False
        },
        'NetworkInterfaces': [
            {
                'AssociatePublicIpAddress': False,
                'DeleteOnTermination': True,
                'SubnetId': spot_subnet,
                'DeviceIndex': 0,
                'Groups': [
                    security_group,
                ],
            },
    ],
    },
    InstanceInterruptionBehavior='terminate',
    SpotPrice=instance_spot_price,
)

# -- Grab Spot Request ID -- #
request_id = instance['SpotInstanceRequests'][0]['SpotInstanceRequestId']

# --  Allow Instance ID Initialization -- #
time.sleep(30)

response_describe_spot = client.describe_spot_instance_requests(
    SpotInstanceRequestIds=[
        request_id,
    ],
)

# -- Grab Newly Created Instance ID -- #
instance_id = response_describe_spot['SpotInstanceRequests'][0]['InstanceId']

#---------------------------#
# ADD TAGS TO SPOT INSTANCE #
#---------------------------#

add_tags = client.create_tags(
    Resources=[
        instance_id,
    ],
    Tags=[
        {
            'Key': 'Name',
            'Value': instance_name,
        },
    ],
)

#--------------------------------------------#
# REGISTER SPOT INSTANCE TO ELB TARGET GROUP #
#--------------------------------------------#

client = boto3.client('elbv2')
register_instance = client.register_targets(
    TargetGroupArn=target_group_arn,
    Targets=[
        {
            'Id': instance_id,
            'Port': 80,
        },
    ]
)