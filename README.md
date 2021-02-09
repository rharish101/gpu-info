# GPU Usage Monitoring

This is a tool to monitor which users are using how much memory overall, per host, and per GPU, on multiple GPU servers.

**NOTE**: This only works with servers using NVIDIA's GPUs.

## Setup
You need to setup SSH key-based authentication on the GPU servers before using this script.

## Instructions
This script uses argparse to parse commandline arguments.
Thus, to know the available CLI options, run:
```
./gpu_info.py --help
```

To run the script:
1. Change the working directory to the root of this repository.
2. Run `gpu_info.py` on your local desktop as follows:
    ```
    ./gpu_info.py HOSTNAME [HOSTNAME...]
    ```

