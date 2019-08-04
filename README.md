# Availability on the Spot
An EC2 Spot instance is spare compute capacity available from AWS with up to a 90% discount. By using spot instances we are able to substantially reduce costs and scale-up our application with ease. There are, however, other implementation challenges in using spot instances. Since spot instances are spare compute power, AWS may remove these resources from the available pool at anytime, with only a two minute warning. This project allows your to overcome these challenges to provide greater availability on spot instances, with decreased cost.

## How It Works

![elastic load balancer](https://jorgearuiz.net/wp-content/uploads/2019/08/spot2.png)

![elastic load balancer](https://jorgearuiz.net/wp-content/uploads/2019/08/python_boto.jpeg)

![python + boto 3](https://jorgearuiz.net/wp-content/uploads/2019/08/python_boto.jpeg)

![spot ec2](https://jorgearuiz.net/wp-content/uploads/2019/08/spot_ec2.jpeg)

![serverless lambda](https://jorgearuiz.net/wp-content/uploads/2019/08/lambda.jpeg)

### Variables


Instance Running State Codes Table
| Code | State       |
|------|-------------|
|0     |pending      |
|16    |running      |
|32    |shutting-down|
|48    |terminated   |
|64    |stopping     |
|80    |stopped      |
