"""
A Python script which list all files from a tar.gz file located in a S3 bucket. Before use, you must authenticate yourself
with aws-okta or other various authentication methods that set your AWS credentials.

Example: $ python3 ls_tar_ball_s3.py cdp-ghe-backup-tools-staging-us 20200617T202937.tar.gz
"""
#!/usr/bin/python
import boto3
import io
import tarfile
import sys

if __name__ == "__main__":
    if sys.argv[1] is not None:
        bucket_name = sys.argv[1]
    else:
        bucket_name = input("Please type in the name of the bucket: ")
    if sys.argv[2] is not None:
        file_name = sys.argv[2]
    else:
        file_name = input("Please type in the tar file name: ")

    try:
        s3client = boto3.client("s3")
        s3_object = s3client.get_object(Bucket=bucket_name, Key=file_name)
        wholefile = s3_object["Body"].read()
        fileobj = io.BytesIO(wholefile)
        tarf = tarfile.open(fileobj=fileobj)
        names = tarf.getnames()
        for name in names:
            print(name)
    except Exception as e:
        print("There was an error...")
        raise e
