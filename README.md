# Availability on the Spot
An EC2 Spot instance is spare compute capacity available from AWS with up to a 90% discount. By using spot instances we are able to substantially reduce costs and scale-up our application with ease. There are, however, other implementation challenges in using spot instances. Since spot instances are spare compute power, AWS may remove these resources from the available pool at anytime, with only a two minute warning. This solution allows us to overcome these challenges to provide greater availability on spot instances, with decreased costs.

## How It Works
Using a combination of AWS services we are able to achieve highly available and cost effective infrastructure.

![High Available Infrastructure](https://jorgearuiz.net/wp-content/uploads/2019/08/spot2.png)
Every time the user makes a request to our web appiclation, the request is then resolved by aws' DNS service (Route 53). The request is resolved to an application load balancer which then redirects the request among a set of spot ec2 instances. Once an 2 minute spot termination warning is issued, CloudWatch Events will then trigger a Lambda function which will execute the code that will deploy an additional spot instance. This ensure that we maintain a highly available and fault tolerant environment at an affordable price.


![spot ec2](https://jorgearuiz.net/wp-content/uploads/2019/08/spot_ec2.jpeg)
**Spot Elastic Compute Cloud (EC2)** instances provide us with compute resources that are affordable. Using spot instances can provide us with discounts of up to 80-90%. Spot prices flunctuate separately in every zone, meaning that spot prices from us-east-2a will likely differ from those in us-east-2b. Spot resources are based on a bidding system, which means that at any point, AWS can take away your spot resources if another AWS customer is willing to pay more. If this occurs, AWS will provide you with a 2 minute **Spot Termination warning** and will then take away your resources once that 2 minute window ends. 

> Spot resources are best for workloads that can be interrupted; however, through the combination of other services we can achieve high available and fault tolerant infrastructure.

![elastic load balancer](https://jorgearuiz.net/wp-content/uploads/2019/08/ELB.jpeg)
One of the main components in this implementation is the **Elastic Load Balancer (ELB)**. This service will allow us to distribute incoming requests among a set of registered spot ec2 instances. These ec2 instances are part of a target group. Any incoming request will be sent to instances of this group. This alleviates CPU and memory usage, ensuring that users experience a service that is fast and reliable.

![ELB](https://jorgearuiz.net/wp-content/uploads/2019/08/elb-1.jpg)

> It is recommended that you use an **Application Load Balancer (ALB)** if you are planning of serving a web application. ALBs are best suited for load balancing HTTP and HTTPS traffic.

![serverless lambda](https://jorgearuiz.net/wp-content/uploads/2019/08/lambda.jpeg)
**Serveless Lambda** plays a important role in implementing a highly available and fault tolerant infrastructure using spot instances. As previously mentioned, whenever AWS is about to take away your Spot EC2 instances, you are provided with a 2 minute Spot Termination warning. Using Lambda, we can acknowledge the Spot termination warning using CloudWatch Events. This warning then triggers a lambda function that will allow us to be proactive and take action. This ensures that users do not experience unreliable web services due to a unhealthy instance.

![python + boto 3](https://jorgearuiz.net/wp-content/uploads/2019/08/python_boto.jpeg)
Once our Lambda function is triggered by a CloudWatch Event, it will then execute our **Python code**. Using **Boto 3**, we can access our AWS environment and manage our resources. Our Python code will perform a series of steps that will ensure that a new Spot instance is deployed.

#### Determining Zone To Deploy Instance
This step will list resources in our subnets within our Virtual Private Cloud (VPC). Our main goal is to ensure that we deploy our new instance in a subnet that currently does not contain another Spot EC2 instance. This is to ensure that we distribute our Spot EC2 instances across our Availability Zones and achieve high availability. We want to avoid the problem of having multiple Spot EC2 instance being removed at once due to a Spot price change.

#### Getting Spot Price
This step is very simple, we simply make a request to get the latest Spot price for the Availability Zone that have chosen to use for our Spot EC2 instance deployment. We will use this price for our bidding.

#### Request Spot Price
During this step we will be making the actual Spot EC2 request. For this step to be successful, we have to ensure that we provide the appropriate details to ensure we get the instance we wish to deploy. 

We need details such as:
+ Instance type
+ Security groups
+ Amazon Machine Image (AMI)
+ Keypairs
+ Spot price

#### Tag Spot Instances
Once our request has been fulfilled successfully, we need to ensure that we provide the appropriate tags to our Spot EC2 instance. Tagging our instance will allow us to identify the Spot EC2 instance from other instances when executing the lambda function; it will serve as an identifier. 

The following table provides the naming convention according to the Availabity Zone we want to deploy.
For example, if our server name is Prometheus and we will be using all Availability Zones within the Ohio region, our Spot EC2 instances will be named (tagged) as follows.
  
|Server Name |Availability Zone|
|:-----------|:----------------|
|Prometheus-A|us-east-2a|
|Prometheus-B|us-east-2b|
|Prometheus-C|us-east-2c|

#### Registering Spot Instance to Target Group
Once we have successfully deployed our instance, it is important that we register it to our Target Group. This will ensure that we distribute any incoming HTTPS/HTTPS requests through an elastic load balancer.

### Variables

| Variable | |
|:---------|-|
|REGION|The region in which you wish to deploy and access AWS resources.|
|instance_name|Base name of your instance. For example: MyWebsite|
|instance_prefix|Name prefix, allows you to identify in which zone your instance has been deployed. For example: Prometheus-A, this allows you to quickly identify that your instance is in zone A.|
|key_pairs|Keypairs to assign to instance.|
|instance_type|Instance type. For example: t2.micro|
|instance_description| Instance description, required to specify operating system.|
|ami_id|AMI id|
|number_of_subnets|Number of subnets in your VPC in which you wish to deploy new instance.|
|subnets_id_list|List of subnet ids. Must correlate with number_of_subnets.|
|zones| List of zones within your region, for example, us-east-2a us-east-2b us-east-2c if you want to deploy in us-east-2. Must correlate with number_of_subnets.|
|security_group|Security group id|
|target_group_arn|Amazon Resource Name of your target group. Required to register new instance.|
|name_tag_index|EC2 tag index array containing the name of the instance, which will serve as the identifier.|


Instance Running State Codes Table

| Code | State       |
|:-----|:------------|
|0     |pending      |
|16    |running      |
|32    |shutting-down|
|48    |terminated   |
|64    |stopping     |
|80    |stopped      |

## Compatibility
Python v3.6

## Backlog
- [ ] Balance deployments per zone
- [ ] Ability to automate deployment of instances until count is met
- [ ] Terraform configuration files for automating infrastructure provisioning
- [ ] Terraform destroy capabilities for instances
- [ ] Ansible playbook for automating configuration management
