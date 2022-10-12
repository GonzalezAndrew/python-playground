from datetime import datetime
from datetime import timedelta
from datetime import timezone

snapshot = {
    "AvailabilityZones": [
        "us-east-1a",
        "us-east-1a",
        "us-east-1b",
        "us-east-1b",
        "us-east-1d",
        "us-east-1d",
    ],
    "DBClusterSnapshotIdentifier": "rds:",
    "DBClusterIdentifier": "eks-cluster",
    "SnapshotCreateTime": "2022-06-14 08:50:26.151000+00:00",
    "Engine": "aurora-postgresql",
    "EngineMode": "provisioned",
    "AllocatedStorage": 186,
    "Status": "available",
    "Port": 0,
    "VpcId": "vpc-0000000",
    "ClusterCreateTime": "2022-04-22 20:04:06.580000+00:00",
    "MasterUsername": "postgresql",
    "EngineVersion": "13.10",
    "LicenseModel": "postgresql-license",
    "SnapshotType": "automated",
    "PercentProgress": 100,
    "StorageEncrypted": "true",
    "KmsKeyId": "arn:aws:kms:us-east-1:0000000000:key/00000000b-0a0a0-0a0a-0a0a-0a0a0aa0a0a0aa0",
    "DBClusterSnapshotArn": "arn:aws:rds:us-east-1:0000000000:cluster-snapshot:rds:eks-cluster-2022-06-14-08-50",
    "IAMDatabaseAuthenticationEnabled": "false",
    "TagList": [],
}

snapshot_create_time = snapshot["SnapshotCreateTime"]

date_obj = datetime.fromisoformat(snapshot_create_time)

print(repr(date_obj))

today = datetime.now(timezone.utc)
expire = today - timedelta(90)


print(repr(expire))


results2 = date_obj - expire
results = expire - date_obj
print(repr(results))
if results.days <= 0:
    print("ye")

print(results.days)
print(results2.days)
