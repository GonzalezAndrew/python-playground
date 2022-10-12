import boto3
import csv
import json
from datetime import datetime

accounts = {
    "671758882420": "liveoak-sandbox",
    "598248337194": "liveoak-staging",
    "421922515484": "statefarm",
    "9964960881": "liveoak-tech",
    "769657045127": "loa-sf",
    "312865631970": "liveoak-dev",
}

data = {}


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


with open("DCSRE-524.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        accountId = row["Subscription ID"]
        if accountId in data:
            data[accountId].append(row)
        else:
            data[accountId] = []
            data[accountId].append(row)
    file.close()

with open("data.json", "w") as out:
    json.dump(data, out, indent=4)

header = ["Role Name", "Last Used", "Attached Policies"]


for account in data:
    profile = accounts[account]
    session = boto3.Session(profile_name=profile)
    client = session.client("iam")
    print(f"\nRunning on the account: {profile}")
    with open(f"{profile}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        outer_data = []
        for i in data[account]:
            inner_data = []
            role_name = i["Resource Name"]
            inner_data.append(role_name)
            print(f"Role Name: {role_name}")
            response = client.get_role(RoleName=role_name)
            if "RoleLastUsed" in response["Role"]:
                if "LastUsedDate" in response["Role"]["RoleLastUsed"]:
                    lastUsedDate = response["Role"]["RoleLastUsed"]["LastUsedDate"]
                    print(f"\tlast used: {lastUsedDate}")
                    inner_data.append(lastUsedDate)
                elif len(response["Role"]["RoleLastUsed"]) == 0:
                    print(f"\tlast used: never")
                    inner_data.append("never")
            else:
                print(f"\tlast used: never")
                inner_data.append("never")
            resp = client.list_attached_role_policies(RoleName=role_name)
            if "AttachedPolicies" in resp:
                if len(resp["AttachedPolicies"]) != 0:
                    attached_policies = [
                        a["PolicyName"] for a in resp["AttachedPolicies"]
                    ]
                    attached_policies = ",".join(attached_policies)
                    print(f"\tattached policies: {attached_policies}")
                    inner_data.append(attached_policies)
                else:
                    print("\tNo attached policies")
                    inner_data.append("None")
            else:
                print("\tNo attached policies")
                inner_data.append("None")
            outer_data.append(inner_data)
        writer.writerows(outer_data)
