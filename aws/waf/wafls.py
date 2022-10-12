import boto3
from datetime import datetime
import argparse

import os
import sys
from typing import Optional
from typing import Sequence

from rich.console import Console
from rich.table import Table

"""
A simple Python script which will output the IP cidr blocks from WAF rules.

Package Requirements:
    pip install boto3 rich

Usage:
    # set aws profile and region
    python3 wafls.py --profile liveoak-tech --region us-east-1

    # use environment variables
    python3 wafls.py 

Example output:

        WAF Rule:
   DCSRE-885-212_30_33
┏━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Type ┃          Value ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━┩
│ IPV4 │ 212.30.33.0/24 │
└──────┴────────────────┘

         WAF Rule:
    docusign_whitelist
┏━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Type ┃            Value ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ IPV4 │  64.207.216.0/22 │
│ IPV4 │ 209.112.104.0/22 │
│ IPV4 │  185.81.100.0/22 │
│ IPV4 │ 162.248.184.0/22 │
└──────┴──────────────────┘

                  WAF Rule: tenable
┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Type ┃                                      Value ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ IPV4 │                            54.255.254.0/26 │
│ IPV4 │                          54.219.188.128/26 │
│ IPV4 │                          54.175.125.192/26 │
│ IPV4 │                           3.124.123.128/25 │
│ IPV4 │                            18.194.95.64/26 │
│ IPV4 │                             3.132.217.0/25 │
│ IPV4 │                            13.56.21.128/25 │
│ IPV4 │                             13.59.252.0/25 │
│ IPV4 │                           3.106.118.128/25 │
│ IPV4 │                            35.177.219.0/26 │
│ IPV4 │                            13.115.104.0/24 │
│ IPV4 │                             3.9.159.128/25 │
│ IPV4 │                             34.223.64.0/25 │
│ IPV4 │                           54.93.254.128/26 │
│ IPV4 │                          44.242.181.128/25 │
│ IPV4 │                             13.210.1.64/26 │
│ IPV4 │                            18.139.204.0/25 │
│ IPV4 │                          34.201.223.128/25 │
│ IPV4 │                            35.182.14.64/26 │
│ IPV6 │ 2600:1f18:614c:8000:0000:0000:0000:0000/56 │
│ IPV6 │ 2406:da1c:020f:2f00:0000:0000:0000:0000/56 │
│ IPV6 │ 2600:1f14:0141:7b00:0000:0000:0000:0000/56 │
│ IPV6 │ 2406:da18:0844:7100:0000:0000:0000:0000/56 │
│ IPV6 │ 2a05:d014:0532:0b00:0000:0000:0000:0000/56 │
│ IPV6 │ 2600:1f1c:013e:9e00:0000:0000:0000:0000/56 │
│ IPV6 │ 2406:da14:0e76:5b00:0000:0000:0000:0000/56 │
│ IPV6 │ 2600:1f16:08ca:e900:0000:0000:0000:0000/56 │
│ IPV6 │ 2600:1f11:0622:3000:0000:0000:0000:0000/56 │
│ IPV6 │ 2a05:d01c:0da5:e800:0000:0000:0000:0000/56 │
└──────┴────────────────────────────────────────────┘

"""


def output_table(title: str, data: list) -> int:
    """output data into table."""
    console = Console()
    table = Table(title=f"WAF Rule: {title}", style="bold")

    table.add_column("Type", style="bold magenta")
    table.add_column("Value", justify="right", style="bold cyan")

    for info in data:
        table.add_row(info.get("Type"), info.get("Value"))

    console.print(table)
    console.print()

def waf_ls(session: boto3.session.Session, region: str) -> int:
    """Output IP Sets for all WAF rules in the given AWS region.
    :param session: The AWS boto3 session object.
    :param region: The AWS region to connect to.
    :return: None
    :rtype: none
    """
    client = session.client("waf-regional", region)
    response = client.list_ip_sets()
    ip_sets = response["IPSets"]
    for ip_set in ip_sets:
        ip_set_id = ip_set["IPSetId"]
        resp = client.get_ip_set(IPSetId=ip_set_id)
        ip_set_desc = resp["IPSet"]["IPSetDescriptors"]
        ip_set_desc = sorted(ip_set_desc, key=lambda x: x["Type"])
        ip_set_name = resp["IPSet"]["Name"]
        output_table(ip_set_name, ip_set_desc)


def run(args: argparse.Namespace) -> int:
    """delegation function"""
    if args.profile:
        profile = args.profile
    elif "AWS_PROFILE" in os.environ:
        profile = os.environ["AWS_PROFILE"]

    # create boto3 session obj
    session = boto3.Session(profile_name=profile)

    if args.region:
        region = args.region
    elif "AWS_REGION" in os.environ:
        region = os.environ["AWS_REGION"]
    else:
        # if neither region are set, get default region from aws profile
        region = session.region_name

    waf_ls(session=session, region=region)


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="wafls",
        description="A command line tool used to list all waf ip sets in all rules.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--profile",
        type=str,
        help="The AWS profile to use for authentication. Will use the environment variable `AWS_PROFILE` by default.",
    )

    parser.add_argument(
        "--region",
        type=str,
        help="The AWS region where WAF rules are located. Will use the environment variable `AWS_REGION` or the default AWS region for the profile by default.",
    )

    if len(argv) == 0 and "AWS_PROFILE" not in os.environ:
        parser.print_help()

    try:
        args = parser.parse_args(argv)
        run(args)
    except Exception as err:
        raise err


if __name__ == "__main__":
    raise SystemExit(main())
