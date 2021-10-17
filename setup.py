#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")
    ) as fh:
        return fh.read()


setup(
    name="investporto",
    version="0.0.1",
    license="MIT",
    description="Investment portofolio management",
    long_description=read("README.md"),
    author="Sebastian Fischer",
    author_email="",
    url="https://github.com/ionelmc/python-nameless",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    keywords=[
        "investment",
        "portofolio",
        "tool",
    ],
    python_requires=">=3.6",
    install_requires=[
        "click",
        "pyyaml",
    ],
    tests_require=["pytest", "pytest-mock", "coverage"],
    extras_require={},
    setup_requires=[],
    entry_points={
        "console_scripts": [
            "investporto = investporto.cli:main",
        ]
    },
)
