﻿from setuptools import setup, find_packages

dependencies = [
    "ultralytics>=8.0.237",
    "matplotlib>=3.3.0",
    "numpy>=1.22.2",
    "opencv-python>=4.6.0",
    "pillow>=7.1.2",
    "pyyaml>=5.3.1",
    "requests>=2.23.0",
    "scipy>=1.4.1",
    "torch>=1.8.0",
    "torchvision>=0.9.0",
    "tqdm>=4.64.0", # progress bars
    "psutil", # system utilization
    "py-cpuinfo", # display CPU info
    "thop>=0.1.1", # FLOPs computation
    "pandas>=1.1.4",
    "seaborn>=0.11.0", # plotting
]

setup(
    name='UnityPythonInteractiveGame_SaveTheTurtles',
    version='1.0',
    packages=find_packages(),
    install_requires=dependencies
)
