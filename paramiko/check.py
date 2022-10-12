import contextlib
import datetime
import os
import time
import traceback
from typing import Generator

import boto3

import paramiko


@contextlib.contextmanager
def ssh_client_handler(
    host: str = None,
    private_key_path: str = None,
    user: str = "ec2-user",
    logging: bool = False,
    config: str = "/Users/andrewgonzalez/.ssh/config",
) -> Generator[None, None, None]:
    try:
        if logging:
            today = datetime.datetime.today()
            log_file = "paramiko-" + today.strftime("%Y%m%d-%H-%M-%S") + ".log"
            paramiko.util.log_to_file(log_file)
        # todo
        if config:
            if os.path.exists(os.path.expanduser(config)):
                ssh_config = paramiko.SSHConfig()
                user_config_file = os.path.expanduser(config)
                with open(user_config_file) as f:
                    ssh_config.parse(f)
            user_config = ssh_config.lookup(host)
            print(user_config)

        private_key = open(private_key_path)
        key = paramiko.RSAKey.from_private_key(private_key)
    except (paramiko.ssh_exception.PasswordRequiredException) as e:
        print("[-] your key is encrypted.")

    ssh_client = paramiko.SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, pkey=key)
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


def get_slave_ips():
    client = boto3.client("ec2")
    ips = []
    custom_filter = [
        {
            "Name": "tag:jenkins_server_url",
            "Values": ["https://jenkins.cicd.cloud.fpdev.io/"],
        },
        {"Name": "instance-state-name", "Values": ["running"]},
    ]

    response = client.describe_instances(Filters=custom_filter)
    info = response["Reservations"]
    for i in info:
        for instance in i["Instances"]:
            if len(instance["NetworkInterfaces"]) != 0:
                for ip in instance["NetworkInterfaces"]:
                    print(ip["PrivateIpAddress"])
                    ips.append(ip["PrivateIpAddress"])
    return ips


def main() -> int:
    ips = get_slave_ips()
    for ip in ips:
        with ssh_client_handler(
            host=ip,
            private_key_path="/Users/andrewgonzalez/.ssh/keys/work/aws-main.pem",
        ) as ssh_client:
            outputs = run_remote_command(
                ssh_client=ssh_client,
                command="docker --version",
            )
            print("Results:")
            for output in outputs:
                print(output)


if __name__ == "__main__":
    exit(main())
