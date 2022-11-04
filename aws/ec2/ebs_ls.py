import csv
import json
from datetime import datetime

import boto3
import botocore

"""
creation date | aws region | state | volume id
"""


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def get_all_profiles():
    """Return a list of profiles from your aws configuration."""
    return boto3.session.Session().available_profiles


def get_all_regions():
    """ """
    try:
        client = boto3.client("ec2")
        return [region["RegionName"] for region in client.describe_regions()["Regions"]]
    except Exception as err:
        raise err


def get_all_ebs_volumes(client):
    try:
        region_name = client._client_config.region_name
        volumes = []
        all_volumes = (
            client.get_paginator("describe_volumes")
            .paginate()
            .build_full_result()["Volumes"]
        )

        for volume in all_volumes:
            create_dateobj = datetime.strftime(
                volume["CreateTime"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            )

            data = {
                "createTime": create_dateobj,
                "awsRegion": region_name,
                "state": volume["State"],
                "volumeId": volume["VolumeId"],
            }
            volumes.append(data)
        return volumes
    except Exception as err:
        raise err


def write_csv(filename, data):
    """write to csv"""
    with open(f"{filename}.csv", "w") as f:
        # wr = csv.writer(f, delimiter=",")
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Created Date",
                "AWS Region",
                "Volume State",
                "Volume ID",
                "Action Items",
            ],
        )
        writer.writeheader()

        for entry in data:
            for info in entry:
                writer.writerow(
                    {
                        "Created Date": info["createTime"],
                        "AWS Region": info["awsRegion"],
                        "Volume State": info["state"],
                        "Volume ID": info["volumeId"],
                        "Action Items": "",
                    },
                )


def main():
    """main"""
    profiles = get_all_profiles()
    regions = get_all_regions()
    # regions = ['us-east-1']
    # profiles = ['liveoak-tech']
    for profile in profiles:
        data = []
        for region in regions:
            session = boto3.Session(profile_name=profile, region_name=region)
            client = session.client("ec2")
            all_volumes = get_all_ebs_volumes(client=client)
            data.append(all_volumes)
        write_csv(filename=profile, data=data)


if __name__ == "__main__":
    raise SystemExit(main())
