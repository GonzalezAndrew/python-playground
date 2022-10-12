import boto3
from rich.console import Console
from rich.table import Table

regions = ["us-east-1", "us-east-2", "eu-west-1", "us-west-2"]
test_regions = ["us-east-1", "us-east-2"]


def output_table(title: str, data: list) -> int:
    """output data into table."""
    console = Console()
    table = Table(title=title, style="bold")

    table.add_column("Repository Name", style="bold magenta")
    table.add_column("ECR Lifecycle Policy", justify="right", style="bold cyan")

    for info in data:
        table.add_row(info.get("repo_name"), info.get("lifecycle_policy"))

    console.print(table)
    console.print()


def get_all_profiles():
    """Return a list of profiles from your aws configuration."""
    return boto3.session.Session().available_profiles


def get_all_repos(client):
    """Get all repositories.
    :param client: The boto3 client object.
    :return: A list of repository names.
    :rtype: list[str]
    """
    try:
        all_repos = (
            client.get_paginator("describe_repositories")
            .paginate()
            .build_full_result()["repositories"]
        )
        all_repos = [
            repos["repositoryName"] for repos in all_repos if "repositoryName" in repos
        ]
        return all_repos
    except Exception as err:
        raise err


def get_ecr_lifecycle_policy(repository_name: str, client):
    """ """
    try:
        response = client.get_lifecycle_policy(repositoryName=repository_name)
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True
    except client.exceptions.LifecyclePolicyNotFoundException:
        return False


def main():
    profiles = get_all_profiles()
    for profile in profiles:
        for region in regions:
            session = boto3.Session(profile_name=profile)
            client = session.client("ecr", region_name=region)
            all_repos = get_all_repos(client=client)

            if len(all_repos) != 0:
                data = []
                for repo_name in all_repos:
                    if get_ecr_lifecycle_policy(
                        repository_name=repo_name,
                        client=client,
                    ):
                        data.append(
                            {"repo_name": repo_name, "lifecycle_policy": "True"},
                        )
                    else:
                        data.append(
                            {"repo_name": repo_name, "lifecycle_policy": "False"},
                        )

                _data = sorted(data, key=lambda x: x["lifecycle_policy"], reverse=True)

                output_table(title=f"{profile}: {region}", data=_data)


if __name__ == "__main__":
    raise SystemExit(main())
