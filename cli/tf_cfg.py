import os
import argparse
from typing import Optional, Sequence
import sys

"""
Configure all the CDP Terraform projects inputs.tfvars under the /projects/ directory of a terraform project

Example: $ cfg create -p tools-dev-us
    #------------------------------------------------------------------------------
    # Project Variables
    #------------------------------------------------------------------------------
    tf_project = "tools-dev-us"
    aws_region = "us-west-2"

"""

CDP = {
    "tools-dev-us": "us-west-2",
    "tools-staging-ap": "ap-northeast-1",
    "tools-staging-ap2": "ap-northeast-2",
    "tools-staging-ap3": "ap-southeast-1",
    "tools-staging-ap4": "ap-southeast-2",
    "tools-staging-ap5": "ap-south-1",
    "tools-staging-ca": "ca-central-1",
    "tools-staging-eu": "eu-west-1",
    "tools-staging-eu2": "eu-west-2",
    "tools-staging-eu3": "eu-west-3",
    "tools-staging-eu4": "eu-north-1",
    "tools-staging-eu5": "eu-central-1",
    "tools-staging-me": "me-south-1",
    "tools-staging-sa": "sa-east-1",
    "tools-staging-us": "us-east-2",
    "tools-staging-us2": "us-east-1",
    "tools-production-ap": "ap-northeast-1",
    "tools-production-ap2": "ap-northeast-2",
    "tools-production-ap3": "ap-southeast-1",
    "tools-production-ap4": "ap-southeast-2",
    "tools-production-ap5": "ap-south-1",
    "tools-production-ca": "ca-central-1",
    "tools-production-eu": "eu-west-1",
    "tools-production-eu2": "eu-west-2",
    "tools-production-eu3": "eu-west-3",
    "tools-production-eu4": "eu-north-1",
    "tools-production-eu5": "eu-central-1",
    "tools-production-me": "me-south-1",
    "tools-production-sa": "sa-east-1",
    "tools-production-us": "us-east-2",
    "tools-production-us2": "us-east-1",
    "tools-govcloud-west": "us-gov-west-1",
}

PROJECTS = [
    "tools-dev-us",
    "tools-staging-ap",
    "tools-staging-ap2",
    "tools-staging-ap3",
    "tools-staging-ap4",
    "tools-staging-ap5",
    "tools-staging-ca",
    "tools-staging-eu",
    "tools-staging-eu2",
    "tools-staging-eu3",
    "tools-staging-eu4",
    "tools-staging-eu5",
    "tools-staging-me",
    "tools-staging-sa",
    "tools-staging-us",
    "tools-staging-us2",
    "tools-production-ap",
    "tools-production-ap2",
    "tools-production-ap3",
    "tools-production-ap4",
    "tools-production-ap5",
    "tools-production-ca",
    "tools-production-eu",
    "tools-production-eu2",
    "tools-production-eu3",
    "tools-production-eu4",
    "tools-production-eu5",
    "tools-production-me",
    "tools-production-sa",
    "tools-production-us",
    "tools-production-us2",
    "tools-govcloud-west",
]

CALLER_DIR = os.getcwd()
ROOT_DIR = "".join([os.getcwd(), "/projects"])


def _validate_project(project: str) -> bool:
    if project not in PROJECTS:
        raise ValueError(f"The project {project} does not exists. Try again.")
    else:
        return project


def _write_to_file(dir: str = "", project: str = "", region: str = "") -> None:
    print(f"Configuring the inputs.tfvars for {dir}...")
    with open(os.path.join(dir, "inputs.tfvars"), "w") as fh:
        _header = "#------------------------------------------------------------------------------\n# Project Variables\n#------------------------------------------------------------------------------\n"
        _project = f'tf_project = "{project}"\n'
        _region = f'aws_region = "{region}"\n'
        full = _header + _project + _region
        fh.write(full)


def create(args: argparse.Namespace) -> int:
    if not os.path.exists(ROOT_DIR):
        print(f"The root directory does not exists -> {CALLER_DIR}")
    else:
        print(f"Root directory exists -> {ROOT_DIR}")

    if args.all and args.project is None:
        for project, region in CDP.items():
            project_dir = "".join([ROOT_DIR, "/", project])
            print(f"Checking for the project directory is {project_dir}")
            if not os.path.exists(project_dir):
                print(f"The project dir {project_dir} does not exists, creating it")
                os.makedirs(project_dir, exist_ok=True)
                _write_to_file(project_dir, project, region)

    elif args.all is False and args.project is not None:
        project_dir = "".join([ROOT_DIR, "/", args.project])
        region = CDP[args.project]
        print(f"Checking for the project directory is {project_dir}")
        if not os.path.exists(project_dir):
            print(f"The project dir {project_dir} does not exists, creating it")
            os.makedirs(project_dir, exist_ok=True)
            _write_to_file(project_dir, args.project, region)


# TODO
def template(args: argparse.Namespace) -> int:
    """
    gh repo create CDP/[<name>] [flags]
        -y, --confirm               Skip the confirmation prompt
        -d, --description string    Description of the repository
            --enable-issues         Enable issues in the new repository (default true)
            --enable-wiki           Enable wiki in the new repository (default true)
        -g, --gitignore string      Specify a gitignore template for the repository
        -h, --homepage URL          Repository home page URL
            --internal              Make the new repository internal
        -l, --license string        Specify an Open Source License for the repository
            --private               Make the new repository private
            --public                Make the new repository public
        -t, --team name             The name of the organization team to be granted access
        -p, --template repository   Make the new repository based on a template repository
    """
    template_url = "https://github.cicd.cloud.fpdev.io/CDP/template-terraform"


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="tfcfg",
        description="A CLI tool to configure a Terraform Project.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparser = parser.add_subparsers(dest="command")

    # add the create command
    create_parser = subparser.add_parser(
        "create",
        help="Create the projects directory and the appropriate inputs.tfvars file.",
    )

    create_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Create all the project directories and inputs.tfvars file",
    )

    create_parser.add_argument(
        "-p",
        "--project",
        nargs="?",
        type=_validate_project,
        help="Create only a specific project and it's associated inputs.tfvars file.",
    )

    # add help command
    help = subparser.add_parser("help", help="Show help for a specific command.")
    help.add_argument("help_cmd", nargs="?", help="Command to show help for.")

    if len(argv) == 0:
        parser.print_help()

    args = parser.parse_args(argv)

    if args.command == "help" and args.help_cmd:
        parser.parse_args([args.help_cmd, "--help"])
        return 0
    elif args.command == "help":
        parser.parse_args(["--help"])
        return 0

    if args.command == "create":
        return create(args)
    else:
        raise NotImplementedError(f"The command {args.command} is not implemented.")


if __name__ == "__main__":
    SystemExit(main())
