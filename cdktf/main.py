#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack

# for terraform provider
from imports.aws import AwsProvider
from imports.aws.datasources import s3.DataAwsS3Bucket

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # define resources here


app = App()
MyStack(app, "cdktf")

app.synth()
