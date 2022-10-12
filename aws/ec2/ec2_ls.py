"""
A Python Script which list all running EC2 instance in all regions
"""
import logging

import boto3

ec2 = boto3.client("ec2")
response = ec2.describe_regions()
for region in response["Regions"]:
    region_name = region["RegionName"]
    try:
        ec2 = boto3.resource("ec2", region_name)
        running_instance = ec2.instances.filter(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}],
        )
        for instance in running_instance:
            print(instance.tags)
    except Exception as err:
        print(err)
