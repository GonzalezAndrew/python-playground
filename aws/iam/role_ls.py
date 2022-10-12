import json
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from urllib import response

import boto3

today = datetime.now(timezone.utc)
INACTIVITY_DAYS = 90


def check_date(date_to_check, days_to_expire=90):
    expired_date = today - timedelta(days_to_expire)

    if isinstance(date_to_check, str):
        snapshot_date_obj = datetime.fromisoformat(date_to_check)
    else:
        snapshot_date_obj = date_to_check

    try:
        results = snapshot_date_obj - expired_date
        if results.days <= 0:
            return True
        else:
            return False
    except Exception as err:
        print(err)


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


client = boto3.client("iam")


response = client.get_paginator("list_roles").paginate().build_full_result()
all_role_names = [role["RoleName"] for role in response["Roles"]]

# print(json.dumps(response, default=datetime_converter, indent=4))

for role_name in all_role_names:
    response = client.get_role(RoleName=role_name)
    if "RoleLastUsed" in response["Role"]:
        if "LastUsedDate" in response["Role"]["RoleLastUsed"]:
            lastUsedDate = response["Role"]["RoleLastUsed"]["LastUsedDate"]
            if check_date(date_to_check=lastUsedDate, days_to_expire=INACTIVITY_DAYS):
                print(
                    f"The role {role_name}, with lastUsedDate {lastUsedDate} has expired.",
                )
            # else:
            #     print(f"The role {role_name}, with lastUsedDate {lastUsedDate} has not expired.")
