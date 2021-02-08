#!/usr/bin/env python3
"""Get GPU usage over multiple hosts."""
import json
import subprocess
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, Namespace
from getpass import getuser
from typing import Dict, List

from gpu_usage import FREE

USAGE_SCRIPT = "gpu_usage.py"


def print_error(hostname: str, message: str) -> None:
    """Print the error message.

    Args:
        hostname: The hostname for which the error occured
        message: The error message to print
    """
    print(f'Error encountered for host "{hostname}":')
    print(message, end="\n\n")  # adding a blank line after the message


def print_usage(usage: Dict[str, int], indent: int = 2) -> None:
    """Print the usage dictionary."""
    # Sort in decreasing usage order, keeping free at last
    sorted_keys = sorted(
        usage.keys(),
        key=lambda user: usage[user] if user != FREE else -1,
        reverse=True,
    )
    for user in sorted_keys:
        user_name = user if user != FREE else "FREE:"
        print("\t" * indent + f"{user_name}: {usage[user]} MiB")


def print_info(info: Dict[str, List[Dict[str, int]]]) -> None:
    """Print all usage info including overall usage."""
    overall_usage: Dict[str, int] = {}
    for host in info:
        print(f'Host "{host}":')
        host_usage: Dict[str, int] = {}

        for num, gpu in enumerate(info[host]):
            print(f"\tGPU {num} Usage:")
            print_usage(gpu)
            for user in gpu:
                host_usage[user] = host_usage.get(user, 0) + gpu[user]

        print("\tTotal Usage:")
        print_usage(host_usage)
        for user in host_usage:
            overall_usage[user] = overall_usage.get(user, 0) + host_usage[user]
        print("")

    print("Overall Usage:")
    print_usage(overall_usage, indent=1)


def main(args: Namespace) -> None:
    """Run the main program.

    Arguments:
        args: The object containing the commandline arguments
    """
    with open(USAGE_SCRIPT, "r") as usage_file:
        usage_code = usage_file.read()

    cmd = ["ssh"]
    if args.jump_host is not None:
        cmd += ["-J", f"{args.username}@{args.jump_host}"]

    info = {}
    for host in args.hosts:
        try:
            proc = subprocess.run(
                cmd + [f"{args.username}@{host}", "python3"],
                input=usage_code,
                capture_output=True,
                timeout=args.timeout,
                check=True,
                text=True,
            )
        except subprocess.TimeoutExpired:
            print_error(host, "SSH timed out")
        except subprocess.CalledProcessError as ex:
            print_error(host, ex.stderr.strip())
        else:
            info[host] = json.loads(proc.stdout)

    if info:
        print_info(info)
    else:
        exit(-1)


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Get GPU usage over multiple hosts",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "hosts",
        metavar="HOSTNAME",
        type=str,
        nargs="+",
        help="list of hostnames for GPU servers",
    )
    parser.add_argument(
        "-u", "--username", type=str, default=getuser(), help="SSH username"
    )
    parser.add_argument(
        "-J", "--jump-host", type=str, help="jump host for SSH"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=5,
        help="timeout for the entire SSH command",
    )
    main(parser.parse_args())
