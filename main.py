#!/usr/bin/env python
from lib.connection import AWSConnection
from lib.operation import operation

#--------------------------------#
region = 'ap-south-1'
#--------------------------------#

def trigger(event = " ", context = " "):

    ConnectionAWS = AWSConnection()
    op = operation()
 
    ConnectionAWS.initConnection('ec2', region)
    ec2_client = ConnectionAWS.getConnection('ec2')

    InstanceId = event.get('detail').get('instance-id')
    op.instance_details(ec2_client, InstanceId)
    
    ConnectionAWS.initConnection('autoscaling', region)
    asg_client = ConnectionAWS.getConnection('autoscaling')
    op.deregister_ec2(asg_client, InstanceId)
    

if __name__ == '__main__':
    
#     alarm = {
#      "version": "0",
#      "id": "12345678-1234-1234-1234-xxxxxxx",
#      "detail-type": "EC2 Spot Instance Interruption Warning",
#      "source": "aws.ec2",
#      "account": "xxxxxxx",
#      "time": "yyyy-mm-ddThh:mm:ssZ",
#      "region": "ap-south-1",
#      "resources": [
#          "arn:aws:ec2:ap-south-1:xxxxx:instance/i-xxxxxx"
#          ],
#      "detail": {
#          "instance-id": "i-xxxxxxxxx",
#          "instance-action": "terminate"
#      }
#  }
    trigger({}, {})
