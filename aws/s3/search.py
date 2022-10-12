import json
from datetime import datetime

import boto3


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


session = boto3.Session()
s3 = boto3.resource("s3")

client = session.client("s3", "us-east-1")

all_buckets = client.list_buckets()["Buckets"]

# print(json.dumps(all_buckets, default=datetime_converter, indent=4))
all_buckets_names = [
    bucket["Name"] for bucket in all_buckets if "trail" not in bucket["Name"]
]

# all_objects = (
#     client.get_paginator("list_objects_v2")
#     .paginate(Bucket=all_buckets_names[0])
#     .build_full_result()
# )
# September 27, 2019 at 11:52 AM CDT
target_date = datetime.fromisoformat(str())

bucket = s3.Bucket(all_buckets_names[0])


def obj_last_modified(myobj):
    return myobj.last_modified


sortedObjects = sorted(bucket.objects.all(), key=obj_last_modified, reverse=True)
print(sortedObjects)
