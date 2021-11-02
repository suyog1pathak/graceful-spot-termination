import boto3
class AWSConnection:

    connection = {}
    resources = {}

    def initConnection(self, resource, region):

        if resource not in self.connection:
            try:
                self.connection[resource] = boto3.client(resource, region_name=region)
            except Exception as e:
                print ("Something went wrong")
                print (e)

    def getConnection(self, resource):
        return self.connection[resource]
#-------------------------------------------------------------------------------------------------------#
    def initResource(self, resource, region):

        if resource not in self.resources:
            try:
                self.resources[resource] = boto3.resource(resource, region_name=region)
                #print(self.resources[resource])
            except Exception as e:
                print("Something went wrong")
                print(e)

    def getResource(self, resource):
        return self.resources[resource]                   