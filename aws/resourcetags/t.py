import boto3
from datetime import datetime
import json


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def get_resources():
    restag = boto3.client("resourcegroupstaggingapi")
    response = restag.get_resources(
        ResourcesPerPage=50, ResourceTypeFilters=["s3:bucket"]
    )
    print(json.dumps(response, default=datetime_converter, indent=4))

    while "PaginationToken" in response and response["PaginationToken"]:
        token = response["PaginationToken"]
        response = restag.get_resources(
            ResourcesPerPage=50,
            PaginationToken=token,
            ResourceTypeFilters=["s3:bucket"],
        )
        print(json.dumps(response, default=datetime_converter, indent=4))


def get_tags_keys():
    restag = boto3.client("resourcegroupstaggingapi")
    response = restag.get_tag_keys()
    print(json.dumps(response, default=datetime_converter, indent=4))

    while "PaginationToken" in response and response["PaginationToken"]:
        token = response["PaginationToken"]
        response = restag.get_tag_keys(PaginationToken=token)
        print(json.dumps(response, default=datetime_converter, indent=4))


def get_tags_values():
    restag = boto3.client("resourcegroupstaggingapi")
    response = restag.get_tag_values(Key="av-status")
    print(json.dumps(response, default=datetime_converter, indent=4))

    while "PaginationToken" in response and response["PaginationToken"]:
        token = response["PaginationToken"]
        response = restag.get_tag_values(PaginationToken=token, Key="av-status")
        print(json.dumps(response, default=datetime_converter, indent=4))


def main():
    tag_filter = [{"Key": "av-status", "Values": ["INFECTED"]}]


if __name__ == "__main__":
    main()
