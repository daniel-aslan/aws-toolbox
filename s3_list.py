import boto3
import argparse, os, base64, re, paramiko, requests, csv
from time import sleep, time, strftime
from pprint import pprint as pp

parser = argparse.ArgumentParser("AWS ToolBox")
parser.add_argument("-ls3", "--list_s3_buckets",
                     action="store_true",
                     help="This flag will list all s3 buckets in aws")
args = parser.parse_args()

s3 = boto3.client('s3')

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

def main():
    if args.list_s3_buckets:
        names = list_all_s3_buckets(s3)
        pp(s3_storage_size(s3, names))

if __name__ == "__main__":
    main()
