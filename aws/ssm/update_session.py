import json
from datetime import datetime

import boto3
import botocore


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def get_all_profiles():
    """Return a list of profiles from your aws configuration."""
    return boto3.session.Session().available_profiles


def get_enabled_regions(boto3_session: boto3.Session, service: str):
    regions = boto3_session.get_available_regions(service)
    enabled_regions = []
    for region in regions:
        sts_client = boto3_session.client("sts", region_name=region)
        try:
            sts_client.get_caller_identity()
            enabled_regions.append(region)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "InvalidClientTokenId":
                # error code received when region is disabled
                # print(f"region {region} is disabled")
                pass
            else:
                raise
    return enabled_regions


for profile in get_all_profiles():
    session = boto3.Session(profile_name=profile)
    regions = get_enabled_regions(session, "ec2")
