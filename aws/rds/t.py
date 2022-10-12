import os
import boto3
import json
from datetime import datetime
from datetime import timezone
from datetime import timedelta

today = datetime.now(timezone.utc)
TARGET_CLUSTER_NAME = os.environ.get("TARGET_CLUSTER_NAME", "stg-us-2")
SOURCE_REGION = os.environ.get("AWS_REGION", "us-east-1")
TARGET_REGION = os.environ.get("TARGET_REGION", "us-east-2")

"""
Lambda needs the following permissions
- kms:ListAliases (IAM policy)
"""


def check_snapshot_expired(snapshot_creation_date, days_to_expire=90):
    """Determines if a snapshot is expired by the given days to expire and the snapshots creation time.
    :param snapshot_creation_date: The creation date of the snapshot in UTC.
    :param days_to_expire: The days to expiration.
    :return: None
    :rtype: null
    """
    expired_date = today - timedelta(days_to_expire)

    if isinstance(snapshot_creation_date, str):
        snapshot_date_obj = datetime.fromisoformat(snapshot_creation_date)
    else:
        snapshot_date_obj = snapshot_creation_date

    try:
        results = snapshot_date_obj - expired_date
        if results.days <= 0:
            # Snapshot has expired. We need to delete
            return True
        else:
            return False
    except Exception as err:
        print(err)


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def get_kms_key(session, region):
    """Finds and returns the AWS managed RDS KMS key id for the target region.
    :param session: The AWS boto3 session object.
    :param region: The AWS region to connect to.
    :return: The AWS RDS managed KMS Key id.
    :rtype: str
    {
        "AliasName": "alias/aws/rds",
        "AliasArn": "arn:aws:kms:us-east-2:000000000000:alias/aws/rds",
        "TargetKeyId": "0000000-0000-0000-0000000000",
        "CreationDate": "2017-10-13 13:56:16.266000-05:00",
        "LastUpdatedDate": "2017-10-13 13:56:16.266000-05:00"
    }
    """
    client = session.client("kms", region)

    try:
        keys = client.list_aliases()
        aliases = keys["Aliases"]
        for alias in aliases:
            if "rds" in alias["AliasName"]:
                print(f"Using the following key {alias}")
                return alias["TargetKeyId"]
            else:
                raise Exception("Unable to find the AWS RDS managed KMS key.")
    except Exception as err:
        print(err)


def get_all_snapshots(session, region):
    """Find and return a list of all snapshots ordered by SnapshotCreateTime.
    :param session: The AWS boto3 session object.
    :param region: The AWS region to connect to.
    :return: A list of all snapshots ordered by SNapshotCreateTime.
    :rtype: list[str]
    """
    try:
        client = session.client("rds", region)
        all_snapshots = (
            client.get_paginator("describe_db_cluster_snapshots")
            .paginate()
            .build_full_result()["DBClusterSnapshots"]
        )
        all_snapshots = [
            snapshot
            for snapshot in all_snapshots
            if TARGET_CLUSTER_NAME in snapshot["DBClusterIdentifier"]
        ]
        return all_snapshots
    except Exception as err:
        print(err)


def delete_snapshot(session, snapshot_id, region):
    """Delete a database cluster snapshot. For more information: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.session.delete_db_cluster_snapshot
    :param session: The AWS boto3 session object.
    :param region: The AWS region to connect to.
    :param snapshot: The databse cluster snapshot id.
    :return: None
    :rtype: null
    """
    client = session.client("rds", region)
    try:
        response = client.delete_db_cluster_snapshot(
            DBClusterSnapshotIdentifier=snapshot_id
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(
                f"Was unsuccessful when trying to delete the snapshot_id: {snapshot_id}"
            )
        return response
    except client.exceptions.InvalidDBClusterSnapshotStateFault as err:
        print(
            f"Invalid database cluster snapshot state. Ensure the snapshot is in the available state. {err}"
        )
    except client.exceptions.DBClusterSnapshotNotFoundFault as err:
        print(f"Database cluster snapshot was not found. {err}")
    except Exception as err:
        print(err)


def copy_snapshot(session, snapshot, target_region, source_region):
    """Copy a database cluster snapshot. For more information: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html#RDS.session.copy_db_cluster_snapshot
    :param session: The AWS boto3 session object.
    :param region: The AWS region to connect to.
    :param snapshot: The database cluster snapshot id.
    :return: None
    :rtype: null
    """
    client = session.client("rds", target_region)

    if snapshot["SnapshotCreateTime"].strftime("%A") == "Friday":
        prefix = "weekly-"
    else:
        prefix = "daily-"

    source_cluster_id = snapshot["DBClusterSnapshotArn"]

    # snapshot["DBClusterSnapshotIdentifier"] looks like -> rds:prod-us-cluster1-2022-05-23-08-32
    # snapshot["DBClusterSnapshotIdentifier"].split(":")[-1] looks like -> prod-us-cluster1-2022-05-23-08-32
    # ex target_snapshot_id: daily-prod-us-cluster1-2022-05-23-08-32
    target_snapshot_id = prefix + snapshot["DBClusterSnapshotIdentifier"].split(":")[-1]

    tags = [
        {"Key": "CopiedBy", "Value": "backup_lambda"},
        {"Key": "SourceRegion", "Value": source_region},
        {"Key": "SourceCluster", "Value": source_cluster_id},
    ]

    # use the aws managed rds kms key for encrypting the copy snapshot
    kms_key_id = get_kms_key(session, target_region)

    try:
        response = client.copy_db_cluster_snapshot(
            SourceDBClusterSnapshotIdentifier=source_cluster_id,
            KmsKeyId=kms_key_id,
            TargetDBClusterSnapshotIdentifier=target_snapshot_id,
            SourceRegion=source_region,
            Tags=tags,
        )

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception("Failed to copy the snapshot to the target region.")
        return response
    except client.exceptions.DBClusterSnapshotAlreadyExistsFault as err:
        print(f"The backup snapshot {target_snapshot_id} already exists. {err}")
    except Exception as err:
        print(err)


def get_most_recent_snapshot(session, region):
    """Get the most recent database cluster snapshot dict.
    :param session: The AWS boto3 session object.
    :param region: The AWS region to connect to.
    :return: The most recent database cluster snapshot dict.
    :rtype: dict{}
    """
    try:
        all_snapshots = get_all_snapshots(session=session, region=region)
        all_snapshots.sort(
            key=lambda all_snapshots: all_snapshots["SnapshotCreateTime"], reverse=True
        )
        return all_snapshots[0]
    except Exception as err:
        print(err)


def clean_old_snapshots(session, region):
    """Delete all database cluster snapshots which are 90 days or 365 days depending on the retention rate.
    :param session: The AWS boto3 session object.
    :param region: The AWS region to connect to.
    :return: None
    :rtype: null
    """
    snapshot_ids = []
    all_snapshots = get_all_snapshots(session=session, region=region)
    all_snapshots.sort(
        key=lambda all_snapshots: all_snapshots["SnapshotCreateTime"], reverse=True
    )

    for snapshots in all_snapshots:
        creation_date = snapshots["SnapshotCreateTime"]
        snapshot_id = snapshots["DBClusterSnapshotIdentifier"]
        prefix = snapshot_id.split("-")[0]

        # if snapshot is weekly retention, check for 365, else 90 days
        if prefix == "weekly":
            days_to_expire = 365
        else:
            days_to_expire = 90

        # check to see if the snapshot has expired yet.
        if check_snapshot_expired(creation_date, days_to_expire=days_to_expire):
            print(
                f"Snapshot {snapshot_id}, with time {creation_date} has expired. Deleting the snapshot."
            )
            snapshot_ids.append(snapshot_id)
            delete_snapshot(session, snapshot_id, region)
        else:
            print(f"Snapshot {snapshot_id}, has not yet expired.")


def lambda_handler(event, context):
    session = boto3.Session()

    # get the most recent snapshot from the source region
    most_recent_snapshot = get_most_recent_snapshot(
        session=session, region=SOURCE_REGION
    )

    # copy the most recent snapshot from the source region to the target region
    copy_snapshot(
        session=session,
        snapshot=most_recent_snapshot,
        target_region=TARGET_REGION,
        source_region=SOURCE_REGION,
    )

    # clean all old snapshots from the target region
    clean_old_snapshots(session=session, region=TARGET_REGION)


if __name__ == "__main__":
    lambda_handler(None, None)
