import boto3
import argparse
from time import sleep
from pprint import pprint as pp

parser = argparse.ArgumentParser("AWS ToolBox")
parser.add_argument("-ls3", "--list_s3_buckets",
                     action="store_true",
                     help="This flag will list all s3 buckets in aws")
parser.add_argument("-ec2", "--list_all_ec2",
                     action="store_true",
                     help="This flag will list all ec2 instances in aws")
parser.add_argument("-ebs", "--list_all_ebs",
                     action="store_true",
                     help="This flag will list all ebs instances in aws")
args = parser.parse_args()

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')

######################################### Regions Functions #####################################
def list_all_regions():
    client = boto3.client('ec2')
    response_reg = client.describe_regions()
    regions = [] 
    response_az = client.describe_availability_zones(
            AllAvailabilityZones=True
            )
    avail_zones = [] 

    for obj in response_reg.get("Regions"):
        regions.append(obj.get("RegionName"))

    for az in response_az.get('AvailabilityZones'):
        avail_zones.append(az.get('ZoneName'))
    
    return regions


########################################### S3 Functions #######################################
def list_all_s3_buckets():
    print("Working")
    client = boto3.client('s3')
    response = client.list_buckets()
    bucket_names = []

    for bucket in response.get('Buckets'):
        bucket_names.append(bucket.get('Name'))

    return bucket_names


def s3_storage_size(bucket_names):
    client = boto3.client('s3')
    bucket_and_size = {}

    for name in bucket_names:
        bucket_size = 0
        #objects = client.list_objects_v2(Bucket=name)
        paginator = client.get_paginator('list_objects_v2')

        for page in paginator.paginate(Bucket=name):
            if "Contents" in page:
                for obj in page.get("Contents",[]):
                    bucket_size += obj['Size']

        bucket_and_size[name] = bucket_size 

    return bucket_and_size


######################################## EC2 Functions #######################################
def list_all_ec2(regions):
    regional_running_instances = {}
    running_instances = []

    for region in regions:
        client = boto3.client('ec2', region_name=region)
        paginator = client.get_paginator('describe_instances')
    
        for page in paginator.paginate(Filters=[
            { 
              'Name': 'instance-state-name',
              'Values': ['running'],
            },
            ],
            ):
            for reservation in page.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    instance_id = instance.get('InstanceId')
                    running_instances.append = instance_id
                    pp(instance_id)
                    pp('-'*50)
        regional_running_instances[region] = running_instances

    return regional_running_instances

  
######################################## EBS Functions #######################################
def list_all_ebs_volumes(regions):
    regional_attached_volumes = {}
    regional_detached_volumes = {}

    for region in regions:
        client = boto3.client('ec2', region_name=region)
        attached_volumes = {}
        detached_volumes = {}
        paginator = client.get_paginator('describe_volumes')
    
        for page in paginator.paginate(Filters=[{
                'Name': 'status',
                'Values': ['in-use'],
               },
              ],
             ):
           ebs_volumes = page.get('Volumes')
           if ebs_volumes:
              for volume in ebs_volumes:
                 attached_volumes[volume.get('VolumeId')] = volume.get('Size')
           else:
              pass
        
        for page in paginator.paginate(Filters=[{
                'Name': 'status',
                'Values': ['available'],
               },
              ],
             ):
           ebs_volumes = page.get('Volumes')
           if ebs_volumes:
              for volume in ebs_volumes:
                 detached_volumes[volume.get('VolumeId')] = volume.get('Size')
           else:
              pass
        
        regional_attached_volumes[region] = attached_volumes
        regional_detached_volumes[region] = detached_volumes

    return regional_attached_volumes, regional_detached_volumes


def main():
    ec2_regions = list_all_regions()

    if args.list_s3_buckets:
        names = list_all_s3_buckets()
        pp(s3_storage_size(names))

    if args.list_all_ec2:
        pp(list_all_ec2(ec2_regions))

    if args.list_all_ebs:
        pp(list_all_ebs_volumes(ec2_regions))


if __name__ == "__main__":
    main()
