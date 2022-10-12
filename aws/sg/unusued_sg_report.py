import json
import os
from datetime import datetime

import boto3
import yaml
from pytablewriter import MarkdownTableWriter


def generate_table_data(data):
    """defer function for generate_md"""
    tables = []
    for profile, v in data.items():
        for i in v:
            if isinstance(i, dict):
                for region, b in i.items():
                    writer = MarkdownTableWriter()
                    writer.table_name = region
                    writer.headers = ["Group Name", "Group Id", "Description"]
                    matrix = []
                    if len(b) != 0:
                        for a in b:
                            values = []
                            description = a.get("Description", "")
                            group_id = a.get("GroupId", "")
                            group_name = a.get("GroupName", "")

                            values.append(group_name)
                            values.append(group_id)
                            values.append(description)
                            matrix.append(values)
                    writer.value_matrix = matrix
                    writer.margin = 1
                    tables.append(writer.dumps())
    return tables, profile


def generate_report_md(filename, data):
    """Sends json data to markdown tables and outputs to markdown file."""
    if not os.path.exists(filename):
        dirpath = os.path.split(filename)
        os.makedirs(dirpath[0], exist_ok=True)

    tables, profile = generate_table_data(data)

    with open(filename, "w") as out:
        out.write(f"# {profile} - Unused Security Groups\n\n")
        for table in tables:
            out.write("%s\n" % table)
    out.close()


def generate_report_json(filename, data):
    """Sends json data to a file."""
    if not os.path.exists(filename):
        dirpath = os.path.split(filename)
        os.makedirs(dirpath[0], exist_ok=True)

    with open(filename, "w") as out:
        json.dump(data, out, default=datetime_converter, indent=4)
    out.close()


def generate_report_yaml(filename, data):
    """converts json to yaml and sends to file"""
    if not os.path.exists(filename):
        dirpath = os.path.split(filename)
        os.makedirs(dirpath[0], exist_ok=True)

    if isinstance(data, str):
        data = json.loads(data)
    else:
        data = json.loads(json.dumps(data))

    with open(filename, "w") as out:
        yaml.dump(data, out, sort_keys=False)
    out.close()


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def check_sg_association(client, sg):
    """Verifys if the given security group contains an associated resource.
        Will return network association if true, else will return false.
    :param client: A boto3 client object.
    :param sg: A security group dict object.
    :return: True and network interface dict if security group contains associations
        or false if security group contains no associations.
    :rtype: True, dict{} | False
    """
    sg_name = sg["GroupName"]
    sg_id = sg["GroupId"]

    response = client.describe_network_interfaces(
        Filters=[
            {"Name": "group-id", "Values": [sg_id]},
        ],
    )

    if len(response["NetworkInterfaces"]) != 0:
        for association in response["NetworkInterfaces"]:
            try:
                data = {
                    "Attachment": association.get("Attachment", ""),
                    "AvailabilityZone": association.get("AvailabilityZone", ""),
                    "Description": association.get("Description", ""),
                    "InterfaceType": association.get("InterfaceType", ""),
                    "NetworkInterfaceId": association.get("NetworkInterfaceId", ""),
                    "PrivateIpAddress": association.get("PrivateIpAddress", ""),
                    "Status": association.get("Status", ""),
                    "SubnetId": association.get("SubnetId", ""),
                    "VpcId": association.get("VpcId", ""),
                }
                print(
                    f"The security group {sg_name} contains the following network associations.",
                )
            except Exception as err:
                raise err
            return True, data
    else:
        print(f"The security group {sg_name} has no network associations.")
        return False


def get_all_sgs(client):
    """Returns a list of all AWS Security Groups.
    :param client: A boto3 client object.
    :return: Returns a list of all AWS Security Groups.
    :rtype: list[dict{}]
    """
    response = client.describe_security_groups()
    return response["SecurityGroups"]


def get_all_profiles():
    """Return a list of profiles from your aws configuration."""
    return boto3.session.Session().available_profiles


def get_acc_id(profile):
    """Return the account number tied to the given profile."""
    session = boto3.Session(profile_name=profile)
    client = session.client("sts")
    try:
        response = client.get_caller_identity()
        acc_num = response.get("Account", "")
        if len(acc_num) != 0:
            return f"{profile} ({acc_num})"
    except Exception as err:
        print(f"Ran into an issue retrieving the {profile} account number. {err}")
        return profile


def main() -> int:
    """main"""

    # get a list of all profiles available to the user who is running the script
    # profiles = get_all_profiles()
    profiles = ["liveoak-tech", "liveoak-sandbox"]
    # list of regions we care about
    regions = ["us-east-1", "us-east-2", "eu-west-1", "us-west-2"]

    for profile in profiles:
        formatted_profile = get_acc_id(profile)
        data = {formatted_profile: []}

        for region in regions:
            print(f"\nRunning on profile: {formatted_profile} in region {region}")

            # create our boto objects which we will pass around to various funcs
            session = boto3.Session(profile_name=profile)
            client = session.client("ec2", region_name=region)

            # storage containers
            no_association = []
            association = []

            # get a list of all sgs
            for sg in get_all_sgs(client):
                # verify the sg is in use
                response = check_sg_association(client=client, sg=sg)

                sg_data = {
                    "Description": sg["Description"],
                    "GroupId": sg["GroupId"],
                    "GroupName": sg["GroupName"],
                }

                # if the sg is not being used, we need to know
                if not response:
                    no_association.append(sg_data)

                else:
                    sg_data["NetworkAssociation"] = response[1]
                    association.append(sg_data)

            data[formatted_profile].append({region: no_association})

        # generate_report_yaml(
        #     filename=f"reports/{profile}.yaml",
        #     data=data,
        # )

        generate_report_md(
            filename=f"reports/{profile}.md",
            data=data,
        )


if __name__ == "__main__":
    raise SystemExit(main())
