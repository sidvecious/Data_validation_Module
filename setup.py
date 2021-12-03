#!/usr/bin/env python

from setuptools import find_packages, setup


def parse_requirements(filename):
    """load requirements from a pip requirements file"""
    line_iterator = (line.strip() for line in open(filename))
    lines = []
    for line in line_iterator:
        if line.startswith("#"):
            continue
        elif line.startswith("git+"):
            repo_name = line.split("/")[-1].split("@")[0]
            lines.append(f"{repo_name} @ {line}")
        else:
            lines.append(line)

    return lines


setup(
    name="data_validation_module",
    version="0.1.11",
    description="A tool with different functions for the data validation",
    author="Lorenzo Olivier",
    author_email="lorenzo.o@seqana.com",
    url="git@gitlab.com:cquest1/prototypes/data_validation_module.git",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=parse_requirements("requirements.txt"),
    zip_safe=False,
    keywords="data_validation_module",
)
