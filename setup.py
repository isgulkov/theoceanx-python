import codecs
import os
import re

from setuptools import find_packages, setup

local_file = lambda *f: \
    open(os.path.join(os.path.dirname(__file__), *f)).read()

root_dir = os.path.abspath(os.path.dirname(__file__))


def get_version(package_name):
    version_re = re.compile(r"^__version__ = [\"']([\w_.-]+)[\"']$")
    package_components = package_name.split('.')
    init_path = os.path.join(root_dir, *(package_components + ['__init__.py']))
    with codecs.open(init_path, 'r', 'utf-8') as f:
        for line in f:
            match = version_re.match(line[:-1])
            if match:
                return match.groups()[0]
    return None


def clean_readme(fname):
    """Cleanup README.me for proper PyPI formatting."""
    with codecs.open(fname, 'r', 'utf-8') as f:
        return ''.join(
            re.sub(r':\w+:`([^`]+?)( <[^<>]+>)?`', r'``\1``', line)
            for line in f
            if not (line.startswith('.. currentmodule')
                    or line.startswith('.. toctree')))


PACKAGE = 'theoceanx-python'

setup(
    name=PACKAGE,
    version=get_version(PACKAGE),
    packages=find_packages(),
    include_package_data=True,
    author='Istomin Ivan Viktorovich',
    author_email="ivan@istomin.im",
    description=(
        "A simple system for structuring a modeler project "
        "architecture via plugin like modules, uses the new "
        "importlib abilities first avalible in python 3.4, "
        "includes an exec load mode for support of python 3.0+"),
    long_description=local_file("README.me"),
    license="MIT",
    keywords=["trading", "cryptocurrency", "exchange", "api", "plugin"],
    url="https://github.com/Ivan-Istomin/theoceanx-python",
    download_url='https://pypi.org/project/theoceanx-python/',
    install_requires=[
        "requests",
        "autopep8",
        "socketIO_client_nexus",
        "web3"
    ],
    tests_require=[
        "nose",
        "pyyaml"
    ],
    extras_require={
        'yaml': 'pyyaml'
    },
    test_suite='nose.collector',

    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ]
)
