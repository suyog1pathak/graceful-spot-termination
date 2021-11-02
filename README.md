# graceful-spot-termination <img src="https://p2zk82o7hr3yb6ge7gzxx4ki-wpengine.netdna-ssl.com/wp-content/uploads/spot-instances.png" width="30px">
![](https://miro.medium.com/max/360/1*qg4GEY91S1IHZ1nXfPCVSg.png)


***How it works ?***

This piece of code has to be deployed as lambda in AWS. Once lambda receive spot interruption warning for any spot ec2 instance in the same region, it will detach the instance from the ASG (indirectly de-registration of ec2 from Target group if any)

***Background***

This is automation is ideal for environments where Spot instances are running in ASG and are behind Target group to serve the traffic. \
Amazon gives spot interruption for spot instance 2 mins before, so it can degrade the user experience as spot ec2 will get terminated abruptly. This can be resolved if we gracefully remove the application/spot-ec2 before the termination so that all running connections can be drained. It is recommended to keep draining time of the target group to 90 sec so that ec2 can get enough space to breathe and get terminated gracefully.  

Cloud watch trigger event
```
{
  "source": ["aws.ec2"],
  "detail-type": ["EC2 Spot Instance Interruption Warning"]
}
```

***Developer contact*** :: suyog1pathak@gmail.com