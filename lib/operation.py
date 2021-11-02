import boto3
from botocore.exceptions import ClientError
import logging

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : [%(filename)s:%(lineno)s - %(funcName)20s()] :%(message)s"
    )
CLOG = logging.getLogger("CLOG")
CLOG.setLevel(logging.INFO)
    
class operation:

#-------------------------------------------#
    instance_properties = {}
#-------------------------------------------#
    def __init__(self):
        """Instance properties should be updated for any new condition based on tags.
         e.g. on which instance(s) this lambda should/shouldn't work"""
        if not bool(self.instance_properties):
            self.instance_properties = {
                "AutoScalingGroup": ""
            }
            CLOG.debug("Constructor set - {}".format(self.instance_properties))

    def instance_details(self, connection, instance_id):
        """Fetching instance tags and creating instance_properties dict"""
        try:
            desc_instance = connection.describe_instances(InstanceIds=[instance_id])
            tags = desc_instance['Reservations'][0]['Instances'][0]['Tags']
            CLOG.debug("Tags fetched for instan {} are as follows - {}".format(instance_id, tags))
            CLOG.info("Instance Details fetched for {}".format(instance_id))
        except ClientError as e:
            CLOG.error( """Unable to describe instance tags \n
                {}""".format(e.response['Error']['Message']))
            raise e    

        for tag in tags:
            if tag['Key'] == 'aws:autoscaling:groupName':
                self.instance_properties["AutoScalingGroup"] = tag['Value']
                CLOG.debug("instance_properties dict appended with - {}".format(tag["Value"]))    

    def deregister_ec2(self, connection, instance_id):
        """Simply detaching instances from ASG if instance_properties is not empty. """
        if len(self.instance_properties.get('AutoScalingGroup')) != 0:
            try:
                res = connection.detach_instances(
                        InstanceIds=[instance_id],
                        AutoScalingGroupName=self.instance_properties.get('AutoScalingGroup'),
                        ShouldDecrementDesiredCapacity=False)
                CLOG.info("Instance {} has been detached from ASG {}".format(instance_id, self.instance_properties.get('AutoScalingGroup')))
                CLOG.debug("Response while detaching instance {} from {} is as below - {}".format(instance_id, self.instance_properties.get('AutoScalingGroup'), res))
            except ClientError as e:
                CLOG.error( "Unable to Detach instance from ASG" + e.response['Error']['Message'])
                raise e
        else:
            CLOG.info("instance_properties seems empty - {}".format(self.instance_properties))    