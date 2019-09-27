# GPU Usage Monitoring

This is used to monitor which users are using how much memory overall, per host, and per GPU, on multiple GPU servers.

**NOTE**: This only works with servers using NVIDIA's GPUs.

## Instructions
1. Setup SSH key authentication on the GPU servers.
2. Place `gpu_info.py` and `gpu_usage.py` in the same directory on your local desktop.
3. Change the working directory to the above directory.
4. Run `gpu_info.py` on your local desktop as follows:
  ```
  ./gpu_info.py HOSTNAME [HOSTNAME...]
  ```
5. Further info can be obtained using:
  ```
  ./gpu_info.py --help
  ```
