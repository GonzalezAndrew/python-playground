import boto3
import json

ec2 = boto3.client("ec2", region_name="us-east-1")

response = ec2.describe_security_groups(
    Filters=[{"Name": "ip-permission.cidr", "Values": ["0.0.0.0/0"]}]
)

sgs = []
for sg in response["SecurityGroups"]:
    name = sg["GroupName"]

    for ip in sg["IpPermissions"]:
        from_port = ip.get("FromPort", "None")
        ip_protocol = ip["IpProtocol"]
        ip_ranges = ip["IpRanges"]
        to_port = ip.get("ToPort", "None")

    output_dict = {
        "GroupName": name,
        "FromPort": from_port,
        "ToPort": to_port,
        "IpProtocol": ip_protocol,
        "IpRanges": ip_ranges,
    }

    sgs.append(output_dict)

for i in response["SecurityGroups"]:
    i.pop("IpPermissionsEgress", None)
    i.pop("Tags", None)

print(json.dumps(response["SecurityGroups"], indent=4))
