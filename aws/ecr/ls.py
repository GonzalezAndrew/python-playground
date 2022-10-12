import csv
import json
import os
from datetime import datetime

import boto3

"""
get a list of repos & images of that repo and when they were last used
ex:
repo_name:
    image_name:image_tag:
        last_used: data

csv:
| repoName | imageTag (imageDigest) | lastRecordedPullTime |

"""
regions = ["us-east-1", "us-east-2", "eu-west-1", "us-west-2"]
test_regions = ["us-east-1", "us-east-2"]


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def get_all_profiles():
    """Return a list of profiles from your aws configuration."""
    return boto3.session.Session().available_profiles


def get_all_images(client, repo_name):
    """Get all images from the given repo name.
    :param client: The boto3 client object.
    :param repo_name: The repository name used to search for images.
    :return: A dictonary of all the images from the given repo name.
    :rtype: dict{}
    """
    try:
        all_images = (
            client.get_paginator("describe_images")
            .paginate(repositoryName=repo_name)
            .build_full_result()["imageDetails"]
        )
        return all_images
    except Exception as err:
        raise err


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


def generate_report_json(filename, data):
    """Sends json data to a file."""
    with open(filename, "w") as out:
        json.dump(data, out, default=datetime_converter, indent=4)
    out.close()


def main():
    """main"""
    all_profiles = get_all_profiles()

    for profile in all_profiles:
        data = {"profile": profile}
        for region in regions:
            print(f"Processing {profile} for region {region}")
            session = boto3.Session(profile_name=profile)
            client = session.client("ecr", region_name=region)
            all_repos = get_all_repos(client=client)

            # if the region doesn't have repos, lets skip it
            if len(all_repos) != 0:
                _repo_data = []  # container to collect repo data
                for repo_name in all_repos:
                    all_images = get_all_images(client=client, repo_name=repo_name)
                    _image_data = []  # container to collect image data for the repo

                    for image in all_images:
                        imageTags = ""
                        imageDigest = ""  # some images don't have tags, so we need to another way of finding them

                        if "imageTags" in image.keys():
                            imageTags = image["imageTags"]
                        else:
                            imageDigest = image["imageDigest"]
                        if "lastRecordedPullTime" in image.keys():
                            lastRecordedPullTime = image["lastRecordedPullTime"]
                        else:
                            lastRecordedPullTime = "Never used"

                        # some images don't have tags...
                        if len(imageTags) != 0:
                            _image_data.append(
                                {
                                    "imageTags": imageTags,
                                    "lastRecordedPullTime": lastRecordedPullTime,
                                },
                            )
                        else:
                            _image_data.append(
                                {
                                    "imageDigest": imageDigest,
                                    "lastRecordedPullTime": lastRecordedPullTime,
                                },
                            )

                    # image_data = {"images": _image_data}

                    _repo_data.append(
                        {"repositoryName": repo_name, "images": _image_data},
                    )
                data[region] = _repo_data
                generate_report_json(f"{profile}.json", data=data)
                print(f"Finished region {region}")


if __name__ == "__main__":
    raise SystemExit(main())
