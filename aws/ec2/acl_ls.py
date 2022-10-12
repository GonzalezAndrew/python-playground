import json
from datetime import datetime
import profile
import boto3
import botocore
import csv


def get_enabled_regions(boto3_session: boto3.Session, service: str):
    regions = boto3_session.get_available_regions(service)
    enabled_regions = []
    # print('gathering a list of enabled regions to search through')
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


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def get_default_vpc(client):
    try:
        response = client.describe_vpcs(
            Filters=[{"Name": "is-default", "Values": ["true"]}]
        )
        return response["Vpcs"][0]["VpcId"]
    except Exception as err:
        return ""


def get_all_profiles():
    """Return a list of profiles from your aws configuration."""
    return boto3.session.Session().available_profiles


def get_wiz_acls():
    acls_wiz = []
    with open("python/aws/ec2/all.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k, v in row.items():
                if k == "Resource Name":
                    acls_wiz.append(v)
    return acls_wiz


profiles = get_all_profiles()
acls_wiz = get_wiz_acls()

for profile in profiles:
    session = boto3.Session(profile_name=profile)
    # print(f'running on {profile}')
    print(f"\n{profile}")

    total = 0
    for region in get_enabled_regions(session, "ec2"):
        client = session.client("ec2", region_name=region)
        defaultVpcId = get_default_vpc(client=client)
        if len(defaultVpcId) != 0:
            response = client.describe_network_acls(
                Filters=[{"Name": "vpc-id", "Values": [defaultVpcId]}]
            )

            # #print(json.dumps(response, default=datetime_converter, indent=4))
            total = total + len(response["NetworkAcls"])

            # print(f"Default vpc in region {region} has a total of {len(response['NetworkAcls'])} network acls")

            for association in response["NetworkAcls"]:
                default = association["IsDefault"]
                vpcId = association["VpcId"]
                aclId = association["NetworkAclId"]
                # print(f'\tdefault vpc id: {vpcId}')
                # print(f'\taclId: {aclId}')
                # print(f"\tIsDefault acl for vpc? {default}")

                if aclId in acls_wiz:
                    # print(f'The {aclId} was marked in wiz and belongs to a default vpc.\n')
                    print(f"\tAWS region {region} -> {aclId}")
                    acls_wiz.remove(aclId)

if len(acls_wiz) != 0:
    print(f"ACLS that do not belong to default VPCS:")
    for acl in acls_wiz:
        print(acl)
# print(f"Total number of ACLs {total}\n")
