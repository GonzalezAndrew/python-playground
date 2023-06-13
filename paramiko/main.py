import argparse
import contextlib
import datetime
import os
import sys
import time
import traceback
from typing import Generator
from typing import Optional
from typing import Sequence

import paramiko


@contextlib.contextmanager
def ssh_client_handler(
    host: str = None,
    private_key_path: str = None,
    user: str = "ec2-user",
    logging: bool = False,
    config: str = None,
) -> Generator[None, None, None]:
    try:
        if logging:
            today = datetime.datetime.today()
            log_file = "paramiko-" + today.strftime("%Y%m%d-%H-%M-%S") + ".log"
            paramiko.util.log_to_file(log_file)
        # todo
        # if config:
        #     if os.path.exists(os.path.expanduser(config)):
        #         ssh_config = paramiko.SSHConfig()
        #         user_config_file = os.path.expanduser(config)
        #         with open(user_config_file) as f:
        #             ssh_config.parse(f)
        #     user_config = ssh_config.lookup(host)
        #     print(user_config)

        private_key = open(private_key_path)
        key = paramiko.RSAKey.from_private_key(private_key)
    except paramiko.ssh_exception.PasswordRequiredException as e:
        print("[-] your key is encrypted.")

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=user, pkey=key)
    try:
        yield ssh_client
    except Exception as e:
        print("*** Connect failed: " + str(e))
        traceback.print_exc()
        exit(1)
    finally:
        ssh_client.close()


def run_remote_command(ssh_client: paramiko.SSHClient, command: str = None) -> list:
    """Run external commands on a target machine.
    :params ssh_client: The SSH Client.
    :params command: The command string that will be run on the target machine.
    :return: A list of outputs from the command.
    :rtype: list[str]
    """
    outputs = []
    try:
        print(f"Running the command {command}...")
        stdin, stdout, stderr = ssh_client.exec_command(command, get_pty=True)
        stdin.close()
        time.sleep(5)

        for line in iter(stdout.readline, ""):
            outputs.append(line.rstrip())

    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        traceback.print_exc()

    return outputs


def get_remote_files(
    ssh_client: paramiko.SSHClient,
    remote_file_path: str = None,
    local_file_path: list = None,
):
    """Use sftp to retrieve remote files from a target machine.
    :params ssh_client: The SSH Client
    :params remote_file_path: The remote file path on the target machine.
    :param local_file_path: The local file path on the host machine.
    :return: 0 | 1
    """
    print("Grabbing files using SFTP")
    sftp = ssh_client.open_sftp()
    try:
        print(
            f"Grabbing the remote file {remote_file_path}, and placing it {local_file_path}",
        )
        sftp.get(remote_file_path, local_file_path)
    except Exception as e:
        print("*** Caught exception: %s: %s" % (e.__class__, e))
        traceback.print_exc()
        return 1

    finally:
        sftp.close()

    return 0


def all_logs(ssh_client: paramiko.SSHClient):
    all_logs = run_remote_command(
        ssh_client=ssh_client,
        command="ls /tmp/ghe_test/logs/",
    )

    for log in all_logs:
        local_path = "".join([os.getcwd(), "/files/logs/", log])
        status = get_remote_files(
            ssh_client=ssh_client,
            remote_file_path=f"/tmp/ghe_test/logs/{log}",
            local_file_path=local_path,
        )
        if status != 0:
            print(f"Exiting with status {status}...")
            exit(status)


def all_reports(ssh_client: paramiko.SSHClient):
    reports_with_failures = run_remote_command(
        ssh_client=ssh_client,
        command="grep -rl 128 /tmp/ghe_test/clone/reports/*",
    )
    for report in reports_with_failures:
        local_path = "".join(
            [os.getcwd(), "/files/reports/reports-", report.split("/report-")[1]],
        )
        status = get_remote_files(
            ssh_client=ssh_client,
            remote_file_path=report,
            local_file_path=local_path,
        )
        if status != 0:
            print(f"Exiting with status {status}...")
            exit(status)


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="cli",
        description="A CLI tool to run commands against the GHE CLI test node.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Add SSH Client logging.",
    )

    parser.add_argument(
        "--host",
        nargs="?",
        type=str,
        help="The hostname for the AWS EC2 node.",
    )

    parser.add_argument(
        "--key",
        nargs="?",
        type=str,
        help="The private key for the AWS EC2 node.",
    )

    parser.add_argument(
        "--config",
        nargs="?",
        type=str,
        default="",
        help="The SSH Config file path  that can be loaded in.",
    )

    subparser = parser.add_subparsers(dest="command")

    # add cmd command
    cmd_parser = subparser.add_parser("command", help="Run a custom command")
    cmd_parser.add_argument(
        "--cmd",
        type=str,
        help="The custom command to run against the AWS EC2 node.",
    )
    cmd_parser.add_argument(
        "--all-logs",
        action="store_true",
        help="Get all application logs.",
    )
    cmd_parser.add_argument(
        "--all-reports",
        action="store_true",
        help="Get all reports.",
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

    if args.command == "command":
        with ssh_client_handler(
            host=args.host,
            private_key_path=args.key,
            logging=args.verbose,
            config=args.config,
        ) as ssh_client:
            if args.all_logs and not args.all_reports:
                all_logs(ssh_client=ssh_client)
            elif args.all_reports and not args.all_logs:
                all_reports(ssh_client=ssh_client)
            elif args.cmd and not args.all_logs and not args.all_reports:
                outputs = run_remote_command(ssh_client=ssh_client, command=args.cmd)
                print("Results:")
                for output in outputs:
                    print(output)


if __name__ == "__main__":
    exit(main())

    """
    python3 t.py --host='10.172.4.220' get --remote-path='/var/opt/jfrog/artifactory/etc/access/keys/root.crt' --local-path='/Users/andrewgonzalez/Documents/GitHub/andrew-gonzalez/python-scripts/artifactory/cert.crt'

    ssh 10.172.4.220 "sudo cat /var/opt/jfrog/artifactory/etc/access/keys/root.crt" > /Users/andrewgonzalez/Documents/GitHub/andrew-gonzalez/python-scripts/artifactory/root.crt
    """
