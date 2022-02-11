#!/usr/bin/env python

import re
import pathlib
import pkg_resources
from setuptools import setup, find_namespace_packages

with pathlib.Path("cccv/__version__").open() as f:
    version = f.read()

with pathlib.Path("requirements.txt").open() as f:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(f)
    ]

setup(
    name="cccv",
    version=version,
    packages=find_namespace_packages(),
    install_requires=install_requires,
    description="",
    author="",
    author_email="",
    url="https://github.com/chriscauley/cccv",
)
