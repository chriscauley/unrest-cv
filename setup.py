#!/usr/bin/env python

import os
from pathlib import Path
import pkg_resources
from setuptools import setup, find_namespace_packages
import re

os.environ['PYTHON_EGG_CACHE'] = '.eggs'

with Path("urcv/__init__.py").open() as f:
    version = re.search('__version__\s*=\s*[\'"](.*)[\'"]\n', f.read()).group(1)

install_requires = [
    'imutils==0.5.4',
    'opencv_python==4.5.5.62',
    'pillow==9.0.1',
    'scikit-learn==1.0.2',
]

setup(
    name="urcv",
    version=version,
    packages=find_namespace_packages(),
    install_requires=install_requires,
    description="",
    author="",
    author_email="",
    url="https://github.com/chriscauley/urcv",
)
