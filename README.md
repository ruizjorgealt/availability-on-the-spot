# Availability on the Spot
An EC2 Spot instance is spare compute capacity available from AWS with up to a 90% discount. By using spot instances we are able to substantially reduce costs and scale-up our application with ease. There are, however, other implementation challenges in using spot instances. Since spot instances are spare compute power, AWS may remove these resources from the available pool at anytime, with only a two minute warning. This project allows your to overcome these challenges to provide greater availability on spot instances, with decreased cost.

## How It Works
Using a combination of AWS service we are able to achieve highly available and cost effective infrastructure.
![High Available Infrastructure](https://jorgearuiz.net/wp-content/uploads/2019/08/spot2.png)

![elastic load balancer](https://jorgearuiz.net/wp-content/uploads/2019/08/ELB.jpeg)
One of the main components in this implementation is the **elastic load balancer**. This service will allow us to distribute incoming requests among a set of registered spot ec2 instances. These ec2 instances are part of a target group. Any incoming request will be sent to instances of this group. This alleviates CPU and memory usage by distrubiting incoming requests.

![ELB](https://jorgearuiz.net/wp-content/uploads/2019/08/elb-1.jpg)

> It is recommended that you use an Application Load Balancer (ALB) if you are planning of serving a web application. ALBs are best suited for load balancing HTTP and HTTPS traffic.

![python + boto 3](https://jorgearuiz.net/wp-content/uploads/2019/08/python_boto.jpeg)

![spot ec2](https://jorgearuiz.net/wp-content/uploads/2019/08/spot_ec2.jpeg)

![serverless lambda](https://jorgearuiz.net/wp-content/uploads/2019/08/lambda.jpeg)

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
