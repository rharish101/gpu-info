<!--
SPDX-FileCopyrightText: 2019 Harish Rajagopal <harish.rajagopals@gmail.com>

SPDX-License-Identifier: MIT
-->

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

To use the script, run it on your local desktop as follows:
```
./gpu_info.py HOSTNAME [HOSTNAME...]
```

## For Contributing
[pre-commit](https://pre-commit.com/) is used for managing hooks that run before each commit, to ensure code quality and run some basic tests.
Thus, this needs to be set up only when one intends to commit changes to git.

1. *[Optional]* Create and activate a virtual environment with Python >= 3.5.
2. Install pre-commit:
    ```sh
    pip install pre-commit
    ```

3. Install pre-commit hooks:
    ```sh
    pre-commit install
    ```

**NOTE**: You need to be inside the virtual environment where you installed the above dependencies every time you commit.
However, this is not required if you have installed pre-commit globally.

## Licenses
This repository uses [REUSE](https://reuse.software/) to document licenses.
Each file has a header containing copyright and license information.
The license files that are used in this project can be found in the [LICENSES](./LICENSES) directory.

The MIT license is placed in [LICENSE](./LICENSE), to signify that it constitutes the majority of the codebase, and for compatibility with GitHub.
