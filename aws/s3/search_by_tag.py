import boto3
from datetime import datetime
import json


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def ls_s3():
    s3 = boto3.resource("s3")
    s3_client = boto3.client("s3")
    bucket = s3.Bucket("loa-staging")
    for obj in bucket.objects.filter(Prefix="46438122"):
        response = s3_client.get_object_tagging(Bucket="loa-staging", Key=obj.key)
        for i in response["TagSet"]:
            if "INFECTED" in i.values():
                print(json.dumps(response, default=datetime_converter, indent=4))
                print(obj.key)


def main():
    ls_s3()


if __name__ == "__main__":
    main()
