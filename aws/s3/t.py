import boto3
import json

"""
report = {
    'us-east-1': [
        {
            'bucket': 'name',
            'replication': 'true',
            'encryption': 'false',
        },
    ]
}
"""


def create_report(data) -> None:
    with open("report.json", "w") as fh:
        fh.write(json.dumps(data, indent=4))
    fh.close()


def bucket_replication_configuration(client, bucket: str) -> bool:
    try:
        resp = client.get_bucket_replication(Bucket=bucket)
        print(f"{bucket} contains replication configuration!")
        return True
    except Exception:
        return False
        # print(f'No replication configuration found for {bucket}')


def bucket_encryption_configuration(client, bucket: str) -> bool:
    try:
        resp = client.get_bucket_encryption(Bucket=bucket)
        print(f"{bucket} contains encryption configuration!")
        return True
    except Exception:
        # print(f'No encryption configuration found for {bucket}')
        return False


def get_all_bucket_names(client) -> str:
    all_buckets = client.list_buckets()["Buckets"]
    return [bucket["Name"] for bucket in all_buckets if "trail" not in bucket["Name"]]


def main() -> int:
    """main"""
    session = boto3.Session()

    # client = session.client("s3", 'eu-west-1')
    # response = client.get_bucket_inventory_configuration(Bucket='loa-production')
    # print(response)

    # regions = session.get_available_regions('s3')
    # report = {}

    # for region in regions:
    #     client = session.client("s3", region)
    #     all_buckets = client.list_buckets()['Buckets']
    #     report[region] = []
    #     for i in all_buckets:
    #         name = i['Name']
    #         data = {
    #             'bucket': name,
    #             'replication': bucket_replication_configuration(client, name),
    #             'encryption': bucket_encryption_configuration(client, name),
    #         }
    #         report[region].append(data)

    # create_report(data=report)


if __name__ == "__main__":
    raise SystemExit(main())
