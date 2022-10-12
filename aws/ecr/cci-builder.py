import argparse
import contextlib
from datetime import datetime
import json
import logging
import os
import sys
from typing import Optional
from typing import Sequence
from typing import Tuple
import urllib3

import boto3

from python_on_whales import docker
from python_on_whales import Image
from python_on_whales.exceptions import DockerException


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("build.log"), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)


def get_latest_agent_version() -> str:
    """Get the latest circleci agent version.
    :return: The latest circleci agent version.
    :rtype: str
    """
    try:
        r = urllib3.PoolManager().request(
            "GET",
            "https://circleci-binary-releases.s3.amazonaws.com/circleci-launch-agent/release.txt",
        )
        agent_version = r.data.decode("utf-8")
        return "".join([i for i in agent_version if i not in [" ", "\t", "\n"]])
    except Exception as err:
        logger.error(
            "There was an error calling `get_latest_agent_version`: \n {}".format(err)
        )
        raise err


@contextlib.contextmanager
def docker_login(registry: str):
    """Context manager for handling the log in and log out process of the docker client.
        refs:
            - https://gabrieldemarmiesse.github.io/python-on-whales/docker_client/#login_ecr
            - https://gabrieldemarmiesse.github.io/python-on-whales/docker_client/#logout
    :param registry: The docker registry to log in to.
    :return: None.
    :rtype: None.
    """
    logger.info(f"Docker logging into the registry {registry}")
    docker.login_ecr(registry=registry)
    try:
        yield
    except Exception as err:
        logger.error("There was an error calling `docker_login`: \n{}".format(err))
        raise err
    finally:
        logger.info(f"Docker logging out of the registry {registry}")
        docker.logout(server=registry)


def docker_build(tag: str, build_args: dict) -> Image:
    """Build a docker image. https://gabrieldemarmiesse.github.io/python-on-whales/sub-commands/buildx/#build
    :param tag: A tag to add to the image.
    :param build_args: The build arguments if any
        ex: build_args={"PY_VERSION": "3.7.8","UBUNTU_VERSION":"20.04"}
    :return: A python_on_wahles.Image object.
    :rtype: python_on_wahles.Image
    """
    try:
        logger.info(
            f"Building the local Dockerfile with the tag {tag} and with the following build arguments {build_args}."
        )
        docker_image = docker.build(
            context_path=".",
            build_args=build_args,
            tags=[tag],
            cache=True,
            platforms=["linux/amd64"],
        )
        return docker_image
    except DockerException as err:
        logger.error("There was an error calling `docker_build`: \n{}".format(err))
        raise err
    except Exception as err:
        logger.error("There was an error calling `docker_build`: \n{}".format(err))
        raise err


def docker_inspect(tag: str) -> Image:
    """Creates a python_on_whales.Image object.
    :param tag: The image tags to inspect.
    :return: A a python_on_whales.Image object.
    :rtype: python_on_whales.Image
    """
    try:
        logger.info(f"Gathering docker image object for {tag}")
        return docker.image.inspect(tag)
    except DockerException as err:
        logger.error("There was an error calling `docker_inspect`: \n{}".format(err))
        raise err
    except Exception as err:
        logger.error("There was an error calling `docker_inspect`: \n{}".format(err))
        raise err


def docker_tag(docker_image: Image, registry: str) -> Image:
    """Tags the docker image for the given AWS ECR registry. https://gabrieldemarmiesse.github.io/python-on-whales/sub-commands/image/#tag
    :param docker_image: The docker image object.
    :param registry: The registry the docker image will be pushed to.
    :return: A python_on_wahles.Image object.
    :rtype: python_on_wahles.Image
    """
    try:
        new_tag = f"{registry}/{docker_image.repo_tags[0]}"

        logger.info(
            "Tagging the image {} -> {}".format(
                docker_image.repo_tags[0], f"{registry}/{docker_image.repo_tags[0]}"
            )
        )

        docker.image.tag(source_image=docker_image, new_tag=new_tag)

        # docker.image.tag returns None, so we need to use docker.image.inspect
        # to generate the image obj
        return docker_inspect(tag=new_tag)
    except DockerException as err:
        logger.error("There was an error calling `docker_build`: \n{}".format(err))
        raise err
    except Exception as err:
        logger.error("There was an error calling `docker_build`: \n{}".format(err))
        raise err


def docker_push(docker_image: Image, registry: str) -> None:
    """Push the docker image to AWS ECR registry. https://gabrieldemarmiesse.github.io/python-on-whales/sub-commands/image/#push
    :param docker_image: The docker image object.
    :param registry: The AWS registry the image will be pushed to.
    :return: None.
    :rtype: None.
    """
    try:
        # ensure we are only pushing the appropriate image to ecr
        if len(docker_image.repo_tags) > 1:
            for tag in docker_image.repo_tags:
                if registry not in tag:
                    docker_image.repo_tags.remove(tag)

        logger.info(
            "Pushing the docker image, {}, to AWS ECR.".format(docker_image.repo_tags)
        )
        docker.image.push(docker_image.repo_tags)
    except DockerException as err:
        logger.error("There was an error calling `docker_build`: \n{}".format(err))
        raise err
    except Exception as err:
        logger.error("There was an error calling `docker_build`: \n{}".format(err))
        raise err


def docker_remove(docker_image: Image) -> None:
    """Remove the docker images from local machine. https://gabrieldemarmiesse.github.io/python-on-whales/sub-commands/image/#remove
    :param docker_image: The docker image object.
    :return: None.
    :rtype: None.
    """
    try:
        logger.info(
            "Removing the image {} from your local machine".format(
                docker_image.repo_tags
            )
        )
        docker.image.remove(docker_image, force=True, prune=True)
    except DockerException as err:
        logger.error("There was an error calling `docker_build`: \n{}".format(err))
        raise err
    except Exception as err:
        logger.error("There was an error calling `docker_build`: \n{}".format(err))
        raise err


def datetime_converter(json_dict):
    """convert datetime in json dict to string."""
    if isinstance(json_dict, datetime):
        return json_dict.__str__()


def get_most_recent_image(
    session: boto3.session.Session, region: str, repository_name: str
) -> dict:
    """Return the most recently pushed image.
    :param session: The AWS boto3 session object.
    :param region: The AWS region to connect to.
    :return: A dictonary
    :rtype: dict{}
    """
    try:
        client = session.client("ecr", region)
        all_images = (
            client.get_paginator("describe_images")
            .paginate(
                repositoryName=repository_name, PaginationConfig={"PageSize": 1000}
            )
            .build_full_result()["imageDetails"]
        )
        all_images.sort(key=lambda full: full["imagePushedAt"], reverse=True)

        logger.info(
            "The most recent image: {}".format(
                json.dumps(all_images[0], default=datetime_converter, indent=4)
            )
        )

        return all_images[0]
    except Exception as err:
        logger.error(
            "There was an error calling `get_most_recent_images`: \n{}".format(err)
        )
        raise err


def update_image_tag(image: dict) -> str:
    """Update the image semantic version and return as string.
    :param image: The AWS ECR image dictonary.
    :return: The updated image tag as a string.
    :rtype: str
    """
    try:
        if "imageTags" in image:
            repository_name = image["repositoryName"]
            logger.info("Updating the tags for the image {}".format(repository_name))
            if len(image["imageTags"]) > 1:
                logger.info(
                    "The image had many tags, selecting the tag with the greatest number. Tag list: {}".format(
                        image["imageTags"]
                    )
                )
                latest_image_version = max(image["imageTags"])
            else:
                latest_image_version = image["imageTags"][0]

            logger.info(
                "Old image tag {}".format(f"{repository_name}:{latest_image_version}")
            )
            # split the str into a list. The tag must look like 0.0.0
            version_split = latest_image_version.split(".")
            version_split[-1] = str(int(version_split[-1]) + 1)
            updated_version = ".".join(version_split)
            logger.info(
                "The updated image tag {}".format(
                    f"{repository_name}:{updated_version}"
                )
            )
            return f"{repository_name}:{updated_version}"
    except Exception as err:
        logger.error("There was an error calling `update_image_tag`: \n{}".format(err))
        raise err


def get_registry_url(image: dict, region: str) -> Tuple[str, str]:
    """Returns a the registry url for the given image. i.e https://aws_account_id.dkr.ecr.region.amazonaws.com
    :param image: The AWS ECR image dictonary.
    :param region: The AWS region the image is located.
    :return: The registry url as a string.
    :rtype: str
    """
    if "registryId" in image and len(region) != 0:
        registryId = image["registryId"]
        logger.info(
            "Registry URL {}, Registry {}".format(
                f"https://{registryId}.dkr.ecr.{region}.amazonaws.com",
                f"{registryId}.dkr.ecr.{region}.amazonaws.com",
            )
        )
        return (
            f"https://{registryId}.dkr.ecr.{region}.amazonaws.com",
            f"{registryId}.dkr.ecr.{region}.amazonaws.com",
        )
    else:
        logger.error(
            "There was an error calling `get_registry_url`.\nThe image dictonary did not contain the `registryId` key."
        )
        raise Exception("The image dictonary did not contain the `registryId` key.")


def run(args: argparse.Namespace) -> int:
    """delegation function"""
    logger.info("Starting the build process.")

    if args.repository_name is None or len(args.repository_name) == 0:
        raise ValueError("You must provide the argument `--repository-name`.")

    if args.profile:
        profile = args.profile
    elif "AWS_PROFILE" in os.environ:
        profile = os.environ["AWS_PROFILE"]

    session = boto3.Session(profile_name=profile)

    if args.region:
        region = args.region
    elif "AWS_REGION" in os.environ:
        region = os.environ["AWS_REGION"]
    else:
        # if neither region are set, get default region from aws profile
        region = session.region_name

    logger.info(f"Using the AWS profile {profile} and the AWS region {region}.")

    build_args = {}
    if args.no_update_agent_version is False:
        build_args["agent_version"] = get_latest_agent_version()

    if args.build_args:
        build_args.update(args.build_args)

    # get the most recent image from the given ecr repo
    image = get_most_recent_image(
        session=session, region=region, repository_name=args.repository_name
    )

    # generate the update image tag
    new_tag = update_image_tag(image=image)

    # get registry url and registry str
    registry_url, registry = get_registry_url(image, region)

    # build, tag, and push the docker image to ecr
    with docker_login(registry=registry_url):
        docker_image = docker_build(tag=new_tag, build_args=build_args)
        tagged_docker_image = docker_tag(docker_image=docker_image, registry=registry)
        logger.debug(
            "The tagged image manifest {}".format(
                json.dumps(tagged_docker_image, default=datetime_converter, indent=4)
            )
        )

        docker_push(docker_image=tagged_docker_image, registry=registry)

        # remove the image specified by user
        if args.remove:
            docker_remove(tagged_docker_image)

    logger.info("The script has finished. Exiting...")


def main(argv: Optional[Sequence[str]] = None) -> int:
    """main"""
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="build",
        description="A command line tool used to build, tag, and push docker images to AWS ECR.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--profile",
        type=str,
        help="The AWS profile to use for authentication. Will use the environment variable `AWS_PROFILE` by default.",
    )
    # # todo
    # parser.add_argument(
    #     "--profiles",
    #     type=list,
    #     help="A list of AWS profiles to use for authentication.",
    # )
    # # todo
    # parser.add_argument(
    #     "--all-profiles",
    #     action="store_true",
    #     help="To run across all AWS profiles configured on your account.",
    # )

    parser.add_argument(
        "--region",
        type=str,
        help="The AWS region where AWS ECR is located. Will use the environment variable `AWS_REGION` or the default AWS region for the profile by default.",
    )
    # # todo
    # parser.add_argument(
    #     "--regions",
    #     type=list,
    #     help="A list of AWS regions where AWS ECR is located. The tool will push the image to all regions listed using this argument.",
    # )
    # # todo
    # parser.add_argument(
    #     "--all-regions",
    #     action="store_true",
    #     help="To run across all AWS regions.",
    # )

    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove the docker image from your local machine once done.",
    )

    parser.add_argument(
        "--no-update-agent-version",
        action="store_true",
        help="To not have the tool update the circleci agent version to the latest version.",
    )

    parser.add_argument(
        "--build-args",
        type=dict,
        help="Pass docker build arguments as a dictonary. i.e `{'arg': 'value'}`",
    )

    # add required arg group for pretty help printing
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--repository-name",
        type=str,
        required=True,
        help="The name of the AWS ECR repository where the image will be uploaded.",
    )

    if len(argv) == 0:
        parser.print_help()

    try:
        args = parser.parse_args(argv)

        run(args)
    except Exception as err:
        logger.error("Unexpected error has occured.")
        raise err


if __name__ == "__main__":
    raise SystemExit(main())
