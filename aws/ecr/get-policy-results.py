import json
from datetime import datetime

import boto3
from rich.console import Console
from rich.table import Table


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def output_table(title: str, data: list) -> int:
    """output data into table."""
    console = Console()
    table = Table(title=f"ECR Preview: {title}", style="bold")

    table.add_column("Image Tags", style="bold magenta")
    table.add_column("Image Pushed Date", justify="center", style="bold cyan")
    table.add_column("Applied Rule Priority", justify="center", style="bold white")

    for info in data:
        table.add_row(
            info.get("imageTags"),
            info.get("imagePushedAt"),
            info.get("appliedRulePriority"),
        )

    console.print(table)
    console.print()


ecr_repo = "loa-app"

session = boto3.Session(profile_name="liveoak-tech")
client = session.client("ecr", region_name="us-east-1")
response = client.get_lifecycle_policy_preview(repositoryName=ecr_repo)

print(json.dumps(response, default=datetime_converter, indent=4))

try:
    results = response["previewResults"]
    data = []
    for result in results:
        imageTags = result["imageTags"]
        imagePushedAt = result["imagePushedAt"]
        appliedRulePriority = result["appliedRulePriority"]

        imagePushedAt = imagePushedAt.strftime("%Y-%m-%d")

        if len(imageTags) != 0:
            imageTags = ", ".join(str(x) for x in imageTags)
        else:
            imageTags = "Untagged"

        data.append(
            {
                "imageTags": imageTags,
                "imagePushedAt": imagePushedAt,
                "appliedRulePriority": str(appliedRulePriority),
            },
        )

    output_table(title=ecr_repo, data=data)
except Exception as err:
    raise err
