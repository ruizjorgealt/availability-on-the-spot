# Availability on the Spot
An EC2 Spot instance is spare compute capacity available from AWS with up to a 90% discount. By using spot instances we are able to substantially reduce costs and scale-up our application with ease. There are, however, other implementation challenges in using spot instances. Since spot instances are spare compute power, AWS may remove these resources from the available pool at anytime, with only a two minute warning. This project allows your to overcome these challenges to provide greater availability on spot instances, with decreased cost.

## How It Works
Using a combination of AWS service we are able to achieve highly available and cost effective infrastructure.
![High Available Infrastructure](https://jorgearuiz.net/wp-content/uploads/2019/08/spot2.png)

![spot ec2](https://jorgearuiz.net/wp-content/uploads/2019/08/spot_ec2.jpeg)
Spot Elastic Compute Cloud (EC2) instances provide us with compute resources that are affordable. Using spot instances can provide us with discounts of up to 80-90%. Spot prices flunctuate separately in every zone, meaning that spot prices from us-east-2a will likely differ from those in us-east-2b. Spot resources are based on a bidding system, which means that at any point, AWS can take away your spot resources if another AWS customer is willing to pay more. If this occurs, aws will provide you with a 2 minute warning and will then take away your resources when that 2 minute window ends. 

> Spot resources are best for workloads that can be interrupted; however, through the combination of other services we can achieve high available and fault tolerant infrastructure.

![elastic load balancer](https://jorgearuiz.net/wp-content/uploads/2019/08/ELB.jpeg)
One of the main components in this implementation is the **elastic load balancer**. This service will allow us to distribute incoming requests among a set of registered spot ec2 instances. These ec2 instances are part of a target group. Any incoming request will be sent to instances of this group. This alleviates CPU and memory usage by distrubiting incoming requests, ensuring that users experience a service that is fast and reliable.

![ELB](https://jorgearuiz.net/wp-content/uploads/2019/08/elb-1.jpg)

> It is recommended that you use an Application Load Balancer (ALB) if you are planning of serving a web application. ALBs are best suited for load balancing HTTP and HTTPS traffic.

![serverless lambda](https://jorgearuiz.net/wp-content/uploads/2019/08/lambda.jpeg)
Serveless lambda plays a important role using in implementing a highly available and fault tolerant infrastructure using spot instances. As previously mentioned, whenever aws is about to take away your spot ec2 instances, you are provided with a 2 minute windows in which you have to take action. Using lambda, we can receive retrieve this warning using CloudWatch Events. This warning then trigger a lambda function that will allow us to be proactive and take action. This ensures that users to do experience downtimes or unreliable web services due to a unhealthy instance.

![python + boto 3](https://jorgearuiz.net/wp-content/uploads/2019/08/python_boto.jpeg)
Once a lambda function starts, it will execute our python code. Using boto 3, we can access our aws environment and manage our resources. Our python code will perform a series of steps that will ensure that a new spot instance is deployed.

#### Determining Zone To Deploy Instance

### Variables


Instance Running State Codes Table

| Code | State       |
|:-----|:------------|
|0     |pending      |
|16    |running      |
|32    |shutting-down|
|48    |terminated   |
|64    |stopping     |
|80    |stopped      |

## Backlog
- [ ] Terraform configuration files for automating infrastructure provisioning
- [ ] Ansible playbook for automating configuration management
