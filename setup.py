#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from os import path as p
import subprocess

try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from distutils.core import setup, find_packages, Command


def read(filename, parent=None):
    parent = (parent or __file__)

    try:
        with open(p.join(p.dirname(parent), filename)) as f:
            return f.read()
    except IOError:
        return ''


def parse_requirements(filename, parent=None):
    parent = (parent or __file__)
    filepath = p.join(p.dirname(parent), filename)
    content = read(filename, parent)

    for line_number, line in enumerate(content.splitlines(), 1):
        candidate = line.strip()

        if candidate.startswith('-r'):
            for item in parse_requirements(candidate[2:].strip(), filepath):
                yield item
        else:
            yield candidate

try:
    from _version import __version__
except ImportError:
    __version__ = "0.1.a1-dirty"

class GitVersionCommand(Command):
    description = 'Extract version from git label'
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        """
        Try to determine the version from git via git describe
        if not possible leave the _version.py file untouched
        """
        message = "Must be in package root {0}".format(self.cwd)
        assert os.getcwd() == self.cwd, message

        version = None
        try:
            version = subprocess.check_output(["git", "describe"])
            version = version[:-1]  # remove the last \r 
        except subprocess.CalledProcessError:
            pass
        if version:
            with open('src/_version.py', 'w') as f:
                f.write("__version__ = '{0}'\n".format(version))


readme = open('README.rst').read()


setup(
    name='cli_tools',
    version=__version__,
    description='Command Line Interface tools',
    long_description=readme + '\n',
    author='Volker Kempert',
    author_email='volker.kempert@pixmeter.com',
    url='www.pixmeter.com',
    package_dir={'': 'src'},
    packages=find_packages(where='src', exclude=[]),
    py_modules = ['_version'],

    install_requires=parse_requirements('requirements.txt'),
    test_requires=parse_requirements('dev_requirements.txt'),
    license="MIT",
    keywords='cli tools',
    classifiers=[
        'Intended Audience :: DevOps',
        'License :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'find-dups=find_duplicates.cli_find_dups:main',
            'filter-dups=find_duplicates.cli_filter_dups:main',
            ]
        },
    cmdclass={ 
              'set_git_version': GitVersionCommand
              },
)
