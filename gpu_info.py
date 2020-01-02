#!/usr/bin/env python3
"""Get GPU usage over multiple hosts."""
import json
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from getpass import getuser
from subprocess import PIPE, Popen, TimeoutExpired

from gpu_usage import FREE

USAGE_CODE = "gpu_usage.py"


def print_usage(usage, indent=2):
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


def print_info(info):
    """Print all usage info including overall usage."""
    overall_usage = {}
    for host in info:
        print(f'Host "{host}":')
        host_usage = {}

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


def main(args):
    """Run the main program.

    Arguments:
        args (`argparse.Namespace`): The object containing the commandline
            arguments

    """
    with open(USAGE_CODE, "rb") as usage_file:
        usage_code = usage_file.read()

    info = {}
    for host in args.hosts:
        proc = Popen(
            [
                "ssh",
                "-o",
                f"ConnectTimeout={args.timeout}",
                f"{args.username}@{host}",
                "python3",
            ],
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
        )

        try:
            output, err = proc.communicate(
                input=usage_code, timeout=args.timeout
            )
        except TimeoutExpired:
            proc.kill()
            output, _ = proc.communicate()
            err = b"Python script timed out"

        if proc.returncode != 0:
            print("-" * 50)
            print(f'Error encountered for host "{host}":')
            print(err.decode("utf8").strip())
            print("-" * 50, end="\n\n")
        else:
            info[host] = json.loads(output.decode("utf8"))

    print_info(info)


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
        "-t",
        "--timeout",
        type=int,
        default=5,
        help="timeout for the entire SSH command",
    )
    main(parser.parse_args())
