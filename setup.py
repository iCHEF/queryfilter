#!/usr/bin/env python
import os.path
from setuptools import find_packages, setup

source_root = os.path.dirname(os.path.abspath(__file__))


def read_requirements_as_package_names():
    """
    Get dependencies listed in a given requirements file.
    1. Packages in 'requirements.txt' are excluded
    2. Lines in `pipenv-requirements.txt` may be empty or starting with '#';
       they should be skipped.
    3. Lines may have post-comment, so they should be spilt by spaces
       and get the first part.
    """
    requirements_path = os.path.join(source_root, "pipenv-requirements.txt")
    with open(requirements_path, "r") as f:
        stripped_lines = (line.strip() for line in f)
        valid_lines = (
            line for line in stripped_lines
            if line and not line.startswith("#") and not line.startswith("-r")
        )
        valid_package_names = [
            line.split()[0].replace(";", "") for line in valid_lines
        ]
        return valid_package_names


setup(
    name="queryfilter",
    version="0.1.0",
    description="Allow same query interface to be shared between Django ORM, SQLAlchemy, and GraphQL backend.",
    long_description=open(os.path.join(source_root, "README.md")).read(),
    license="UNLICENSE",
    url="https://github.com/iCHEF/queryfilter",
    install_requires=read_requirements_as_package_names(),
    tests_require=['pipenv'],  # Use pipenv install --dev
    packages=find_packages(str(source_root)),
    package_data={
        "": ["*.pyi", "*.md"],
    },
    setup_requires=["pytest-runner"],
    classifiers=[
        "iCHEF :: Private",
        "Development Status :: 1 - Planning",
        "Topic :: Database :: Front-Ends",
        "License :: Unlicense",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
