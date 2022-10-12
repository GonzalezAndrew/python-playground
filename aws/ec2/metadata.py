"""
Script which retrieves EC2 Metadata for an AWS EC2 instance

- for local development (not in AWS) use: https://github.com/aws/amazon-ec2-metadata-mock

"""
from typing import Any
from typing import Dict
from typing import Optional

import requests


class EC2Metadata:
    def __init__(self, session: Optional[requests.Session] = None) -> None:
        if session is None:
            session = requests.Session()
        self._session = session
        self.root_url = "http://127.0.0.1:1338/latest/"
        # self.root_url = "http://169.254.169.254/latest/"
        self.dynamic_url = f"{self.root_url}dynamic/"
        self.metadata_url = f"{self.root_url}meta-data/"

    def _request(self, url: str) -> requests.Response:
        resp = self._session.get(url)
        if resp.status_code != 404:
            resp.raise_for_status()
        return resp

    @property
    def instance_identity_document(self) -> Dict[str, Any]:
        return self._request(url=f"{self.dynamic_url}instance-identity/document").json()

    @property
    def account_id(self) -> str:
        return self.instance_identity_document["accountId"]

    @property
    def image_id(self) -> str:
        return self.instance_identity_document["imageId"]

    @property
    def availability_zone(self) -> str:
        return self.instance_identity_document["availabilityZone"]

    @property
    def ram_disk_id(self) -> str:
        return self.instance_identity_document["ramdiskId"]

    @property
    def kernel_id(self) -> str:
        return self.instance_identity_document["kernelId"]

    @property
    def private_ip(self) -> str:
        return self.instance_identity_document["privateIp"]

    @property
    def instance_id(self) -> str:
        return self.instance_identity_document["instanceId"]

    @property
    def instance_type(self) -> str:
        return self.instance_identity_document["instanceType"]

    @property
    def architecture(self) -> str:
        return self.instance_identity_document["architecture"]

    @property
    def region(self) -> str:
        return self.instance_identity_document["region"]


ec2 = EC2Metadata()

# print out all of the obj properties/attributes
for attr in dir(ec2):
    try:
        print("obj.{} = {}".format(attr, getattr(ec2, attr)))
    except AttributeError:
        print("obj.{} = ?".format(attr))
