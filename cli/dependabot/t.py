import argparse
import os
import sys
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import DoubleQuotedScalarString as DQ

"""
A simple script to update the dependabot.yml file. Currently dependabot does not recursively search through directories
meaning every directory in our Terraform monorepo must be listed out in the dependabot.yml file. This script helps autogenerate
the dependabot.yml config file and only includes directory paths which contain .tf files in them.

Install Required Packages:
    pip3 install ruamel.yaml

Example output:
# You can run the script in it's directory or from the root of the repository:
$ python3 update_dbot_cfg.py --dry-run or $ python3 .github/scripts/update_dbot_cfg.py --dry-run

version: 2
updates:
- package-ecosystem: "terraform"
  directory: "/datadog/datadoghq"
  schedule:
    interval: "daily"
- package-ecosystem: "terraform"
  directory: "/datadog/datadoghq/monitors/demo"
  schedule:
    interval: "daily"
- package-ecosystem: "terraform"
  directory: "/datadog/datadoghq/monitors/prod"
  schedule:
    interval: "daily"
"""


def get_dirs(path: str, file_ext: str) -> list:
    """Get a list of directories that only contain the specifed file exstension.
    :param path: The path to search.
    :param file_ext: The file extension to search for.
    :return: A list of directories that only contain the specified file exstension.
    :rtype: list[str]
    """
    dirs = []

    # return nothing if path is a file
    if os.path.isfile(path):
        return []

    # add dir to dirs if it contains .tf files
    if len([f for f in os.listdir(path) if f.endswith(file_ext)]) > 0:
        dirs.append(path)

    for d in os.listdir(path):
        new_path = os.path.join(path, d)
        if os.path.isdir(new_path):
            dirs += get_dirs(path=new_path, file_ext=file_ext)

    return dirs


def generate_yaml_data(
    repo_path: str,
    dirs: list,
    package_ecosystem: str = "terraform",
):
    """Generate the dependabot yaml data which will be written to the dependabot file.
    :param dirs: The directories to add to the dependabot.yml file.
    :package_ecosystem: The package ecosystem.
    :return: A dictonary representing the yaml data that will be written to the dependabot file.
    :rtype: dict{}
    """
    if len(dirs) == 0:
        raise Exception(
            "The list dirs cannot be empty, please ensure the script is correctly gathering the directory information.",
        )

    main_data = {"version": 2, "updates": []}

    for d in dirs:
        # we need to get rid of the absolute path of the repo
        directory = d.replace(repo_path, "")
        if not directory.startswith("/"):
            directory = "/" + directory
        elif directory.startswith("."):
            directory = directory.strip(".")

        data = {
            "package-ecosystem": DQ("terraform"),
            "directory": DQ(directory),
            "schedule": {"interval": DQ("daily")},
        }
        main_data["updates"].append(data)

    return main_data


def yaml_config():
    """config the yaml object and return the object."""
    yaml = YAML()
    yaml.preserve_quotes = True
    return yaml


def find_repo_path(path: str = __file__) -> str:
    """Find the root path of the repository and return it.
    :param path: The path where we should be looking.
    :return: The root path of the repository.
    :rtype: str
    """
    for path in Path(path).parents:
        # Check whether "path/.git" exists and is a directory
        git_dir = path / ".git"
        if git_dir.is_dir():
            return path.as_posix()


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="update-dependabot",
        description="A dirty cli tool for updating the dependabot config file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run a dry run to view changes to dependabot.yml file.",
    )

    parser.add_argument(
        "--update",
        action="store_true",
        help="Update the dependabot.yml config file.",
    )

    yaml = yaml_config()

    repo_root_path = find_repo_path()
    dirs = get_dirs(path=repo_root_path, file_ext=".tf")
    yaml_data = generate_yaml_data(repo_root_path, dirs, "terraform")

    if len(argv) == 0:
        parser.print_help()
        return 1

    try:
        args = parser.parse_args(argv)
        if args.dry_run:
            yaml.dump(yaml_data, sys.stdout)
        elif args.update:
            print("Updating the dependabot.yml file")
            with open(f"{repo_root_path}/.github/dependabot.yml", "w") as file:
                yaml.dump(yaml_data, file)
        else:
            raise Exception("Unexpected argument was passed.")
    except Exception as err:
        raise err


if __name__ == "__main__":
    raise SystemExit(main())
