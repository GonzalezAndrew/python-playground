import csv
import json
from datetime import datetime

import boto3
import yaml


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def get_all_profiles():
    """Return a list of profiles from your aws configuration."""
    return boto3.session.Session().available_profiles


def get_all_users(client):
    try:
        users = client.list_users()
    except Exception as err:
        raise err


def generate_report_json(filename, data):
    """Sends json data to a file."""

    with open(filename, "w") as out:
        json.dump(data, out, default=datetime_converter, indent=4)
    out.close()


def generate_report_yaml(filename, data):
    """converts json to yaml and sends to file"""

    if isinstance(data, str):
        data = json.loads(data)
    else:
        data = json.loads(json.dumps(data))

    with open(filename, "w") as out:
        yaml.dump(data, out, sort_keys=False)
    out.close()


def generate_csv(data):
    profiles = []
    for i in data:
        profiles.append(i["profile"])

    for profile in profiles:
        with open(f"{profile}.csv", "w+") as out:
            writer = csv.DictWriter(
                out,
                fieldnames=["Username", "Description", "Action Items"],
            )
            writer.writeheader()

            for item in data:
                if profile == item["profile"]:
                    for username in item["users"]:
                        writer.writerow(
                            {
                                "Username": username,
                                "Description": "",
                                "Action Items": "",
                            },
                        )


def main():
    # session = boto3.Session(profile_name="liveoak-tech")
    data = []
    for profile in get_all_profiles():
        session = boto3.Session(profile_name=profile)
        client = session.client("iam")

        all_users = (
            client.get_paginator("list_users").paginate().build_full_result()["Users"]
        )
        all_users = [user["UserName"] for user in all_users]

        _data = {"profile": profile, "users": all_users}
        data.append(_data)
        print(json.dumps(_data, default=datetime_converter, indent=4))

    # generate_report_yaml("users.yaml", data)
    # generate_report_json("users.json", data)
    generate_csv(data)


if __name__ == "__main__":
    raise SystemExit(main())
