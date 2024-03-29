#!/usr/bin/env python
import os.path
from setuptools import find_packages, setup

source_root = os.path.dirname(os.path.abspath(__file__))


required_dev = [
    'pytest',
    "coverage",
    "pytest-cov",
    "flake8",
    "pytest-flake8",
    "tox",
    "django",
]


setup(
    name="queryfilter",
    version="0.6.0",
    description=("Allow same query interface to be shared between Django ORM,"
                 "SQLAlchemy, and GraphQL backend."),
    long_description=open(os.path.join(source_root, "README.rst")).read(),
    license="License :: OSI Approved :: Apache Software License",
    url="https://github.com/iCHEF/queryfilter",
    tests_require=['pipenv'],  # Use pipenv install --dev
    packages=find_packages(str(source_root)),
    package_data={
        "": ["*.pyi", "*.rst", "*.md"],
    },
    install_requires=["graphene>=2.0.1,<3", "python-dateutil"],
    setup_requires=["pytest-runner"],
    extras_require={
        'dev': required_dev
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Database :: Front-Ends",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
