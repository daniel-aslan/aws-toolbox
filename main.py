import boto3
import argparse, os, base64, re, paramiko, requests, csv
from time import sleep, time, strftime
from pprint import pprint as pp

parser = argparse.ArgumentParser("AWS ToolBox")
parser.add_argument("-ls3", "--list_s3_buckets",
                     action="store_true",
                     help="This flag will list all s3 buckets in aws")
parser.add_argument("-ec2", "--list_all_ec2",
                     action="store_true",
                     help="This flag will list all ec2 instances in aws")
args = parser.parse_args()

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')

########################################### S3 Functions #######################################
def list_all_s3_buckets(client):
    print("Working")
    response = client.list_buckets()
    bucket_names = []

    for bucket in response.get('Buckets'):
        bucket_names.append(bucket.get('Name'))

    return bucket_names


def s3_storage_size(client, bucket_names):
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
def list_all_ec2(client):
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
    
    for region in regions:
        boto3.setup_default_session(region_name=region)
        paginator = client.get_paginator('describe_instances')
    
        for page in paginator.paginate(Filters=[
            #{ 
            #  'Name': 'instance-state-name',
            #  'Values': ['running'],
            #},
            ],
            ):
           pp(page)
           #pp(type(page.get('Reservations')))


    return regions,avail_zones


def main():
    if args.list_s3_buckets:
        names = list_all_s3_buckets(s3)
        pp(s3_storage_size(s3, names))

    if args.list_all_ec2:
        pp(type(list_all_ec2(ec2)))
        pp(list_all_ec2(ec2))

if __name__ == "__main__":
    main()
