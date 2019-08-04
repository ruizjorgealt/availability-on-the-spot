import boto3
import time
import random
import datetime

#-----------------------------#
# SPOT REQUEST SPECIFICATIONS #
#-----------------------------#

REGION = 'us-west-2'
client = boto3.client('ec2', region_name=REGION)

# -- Instance Description -- #
key_name = instance_name = "name"
instance_prefix = ['-A', '-B', '-C']
instance_type = ''
instance_description = 'Linux/UNIX'
ami_id = ''

# -- VPC Description -- #
subnets_list = ["subnet-a", "subnet-b", "subnet-c"]
zones = ["us-east-2a", "us-east-2b", "us-east-2c"]
security_group = 'sg-id'

# -- ELB Description -- #
target_group_arn = 'elb-arn'

# -- Flags -- #
bool_values = [0,0,0]
name_tag_index = 0

# -- Current Spot Price Values -- #
year = datetime.date.today().year
month = datetime.date.today().month
day = datetime.date.today().day

#-----------------------------------#
# DETERMINE ZONE TO DEPLOY INSTANCE #
#-----------------------------------#

ec2 = boto3.resource('ec2', region_name=REGION)
for x in range(0,3):
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
        if i.tags[name_tag_index]['Value'] == instance_name+instance_prefix[0]:
            print(instance_name+instance_prefix[0])
            bool_values[0] = 1
        elif i.tags[name_tag_index]['Value'] == instance_name+instance_prefix[1]:
            print(instance_name+instance_prefix[1])
            bool_values[1] = 1
        elif i.tags[name_tag_index]['Value'] == instance_name+instance_prefix[2]:
            print(instance_name+instance_prefix[2])
            bool_values[2] = 1

if bool_values[0] == 0:
    print("Launch in zone A")
    spot_subnet = subnets_list[0]
    instance_name = instance_name+instance_prefix[0]
    availability_zone = zones[0]
elif bool_values[1] == 0:
    print("Launch in zone B")
    spot_subnet = subnets_list[1]
    instance_name = instance_name+instance_prefix[1]
    availability_zone = zones[1]
elif bool_values[2] == 0:
    print("Launch in zone C")
    spot_subnet = subnets_list[2]
    instance_name = instance_name+instance_prefix[2]
    availability_zone = zones[2]
else:
    print("Launch in random zone")
    randZone = random.randint(0,2)
    spot_subnet = subnets_list[randZone]
    instance_name = instance_name+instance_prefix[randZone]
    availability_zone = zones[randZone]        

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

#------------------------#
# REQUEST SPOT INSTANCES #
#------------------------#

instance = client.request_spot_instances(
    InstanceCount=1,
    LaunchSpecification={
        'ImageId': ami_id,
        'InstanceType': instance_type,
        'KeyName': key_name,
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