#!/usr/bin/env python3
"""
Setup script for Intent-Based Network Generation Augmentation toolkit.
"""

from setuptools import setup, find_packages
import os

# Read README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="intent-based-network-generation-augmentation",
    version="2.0.0",
    author="Adham Ashraf Eltholth",
    author_email="adham.ashraf@example.com",
    description="A comprehensive toolkit for generating, augmenting, analyzing, and evaluating advanced intent-based networking (IBN) datasets tailored for 5G/3GPP research.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aadhamashraf/Intent-Based-Network-Generation-Augmentation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "gpu": [
            "torch[cuda]>=1.9.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ibn-generate=src.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
)