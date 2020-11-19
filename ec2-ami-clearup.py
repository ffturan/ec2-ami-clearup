import boto3
import sys
import os
import time
from datetime import datetime
from botocore.exceptions import ClientError

def delete_ami(vvWorker,vvAmiId):
  try:
      ami_delete_response = vvWorker.deregister_image(
        ImageId=vvAmiId,
        DryRun=False
      )
      return ami_delete_response
  except ClientError as e:
      print(e)

def delete_snapshot(vvWorker,vvSnapId):
  try:
      snapshot_delete_response = vvWorker.delete_snapshot(
        SnapshotId=vvSnapId,
        DryRun=False
      )
      return snapshot_delete_response
  except ClientError as e:
      print(e)

def find_ami_to_delete(vvWorker,vvDays,vvNow):
    try:
        ami_to_delete={}
        response = vvWorker.describe_images(Owners=['self',])
        for item in response["Images"]:
            ami_id=item["ImageId"]
            snapshot_to_delete=[]
            for subitem in item['BlockDeviceMappings']:
                snapshot_to_delete.append(subitem['Ebs'].get("SnapshotId"))
            creation_date=item["CreationDate"].split("T")
            ami_date=datetime.strptime(creation_date[0], "%Y-%m-%d")
            ami_age=abs((vvNow - ami_date).days)
            if ami_age >= vvDays:
                ami_to_delete.update({str(ami_id): snapshot_to_delete} )
                #ami_to_delete.sort(key=sortSecond)
        return ami_to_delete
    except ClientError as e:
        print(e)

#
# MAIN Starts here
#
def lambda_handler(event, context):
    vDays=os.environ['NUMBER_OF_DAYS']
    # TODAY
    vNow=datetime.today()
    #
    # Connect to AWS
    #
    worker_ec2=boto3.client('ec2')
    result=find_ami_to_delete(worker_ec2,int(vDays),vNow)
    # Key is ami-id
    # Value is list of snapshot-ids
    for key,value in result.items():
        print(f'Deleting {key}')
        delete_ami(worker_ec2,key)
        time.sleep(1)
        for snap in value:
            print(f'Deleting {snap}')
            delete_snapshot(worker_ec2,snap)
