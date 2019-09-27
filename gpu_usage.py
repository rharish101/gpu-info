"""Print usage of each user per GPU."""
import json
from subprocess import check_output
from xml.etree import ElementTree

# Key denoting available memory in a dict where other keys are usernames
FREE = "__free__"

if __name__ == "__main__":
    # Get nvidia-smi's output in XML
    gpu_data = check_output(["nvidia-smi", "-q", "-x"]).decode("utf8")

    xml = ElementTree.fromstring(gpu_data)
    global_usage = []
    for gpu in xml.findall("gpu"):
        local_usage = {}
        local_usage[FREE] = int(
            gpu.find("fb_memory_usage").find("free").text.split()[0]
        )

        for proc in gpu.find("processes").findall("process_info"):
            used_mem = int(proc.find("used_memory").text.split()[0])

            # Get user of this process
            pid = proc.find("pid").text
            user = (
                check_output(["ps", "-o", "user", "-p", pid])
                .decode("utf8")
                .split("\n")[1]
            )

            local_usage[user] = local_usage.get(user, 0) + used_mem

        global_usage.append(local_usage)

    print(json.dumps(global_usage))
