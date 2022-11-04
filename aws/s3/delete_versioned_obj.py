import boto3

"""
Delete a bucket object and ALL it's version. Terraform cannot do this and you cannot delete all versions from the
AWS console...
"""

s3 = boto3.resource("s3")
bucket = s3.Bucket("loa-developuse1-cloudtrail-bucket")
key = "AWSLogs"
object = bucket.object_versions.filter(Prefix=key)
versions = len(list(object.all()))
object.delete()
print(f"Deleted {versions} versions for '{key}'")
