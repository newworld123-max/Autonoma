"""
Setup script for Autonoma.
"""

from setuptools import find_packages, setup

# Read the content of requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="autonoma",
    version="0.1.0",
    description="Decentralized Autonomous AI Agent Platform on Solana",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Autonoma Team",
    author_email="info@autonomaai.online",
    url="https://github.com/autonoma/autonoma",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "autonoma=main:cli_main",
        ],
    },
)
