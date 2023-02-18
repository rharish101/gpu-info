# SPDX-FileCopyrightText: 2019 Harish Rajagopal <harish.rajagopals@gmail.com>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Print usage of each user per GPU."""
import json
from subprocess import check_output
from typing import Dict, List
from xml.etree import ElementTree

# Key denoting available memory in a dict where other keys are usernames
FREE = "__free__"


# NOTE: Type hints are deliberately disabled for this function, because it
# would need too many assert statements to just silence it. The intended
# behaviour is to explicitly fail if the XML isn't as expected.
def get_gpu_usage(gpu):
    """Get the usage info for this GPU.

    Args:
        gpu (ElementTree.Element): The XML element containing info for this GPU

    Returns:
        typing.Dict[str, int]: The usage info for this GPU
    """
    usage = {}
    usage[FREE] = int(gpu.find("fb_memory_usage").find("free").text.split()[0])

    for proc in gpu.find("processes").findall("process_info"):
        used_mem = int(proc.find("used_memory").text.split()[0])

        # Get user of this process
        pid = proc.find("pid").text
        user = (
            check_output(["ps", "-o", "user", "-p", pid])
            .decode("utf8")
            .split("\n")[1]
        )

        usage[user] = usage.get(user, 0) + used_mem

    return usage


def main() -> None:
    """Run the main program."""
    # Get nvidia-smi's output in XML
    gpu_data = check_output(["nvidia-smi", "-q", "-x"]).decode("utf8")
    xml = ElementTree.fromstring(gpu_data)
    global_usage: List[Dict[str, int]] = [
        get_gpu_usage(gpu) for gpu in xml.findall("gpu")
    ]
    print(json.dumps(global_usage))


if __name__ == "__main__":
    main()
