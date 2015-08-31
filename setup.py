#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import path as p

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


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
    __version__ = "0.1.a1"

readme = open('README.rst').read()


setup(
    name='cli_tools',
    version=__version__,
    description='Command Line Interface tools',
    long_description=readme + '\n',
    author='Volker Kempert',
    author_email='volker.kempert@pixmeter.com',
    url='www.pixmeter.com',
    packages=find_packages(),
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
            'find-dups=find_duplicates:main',
            ]
        },
)
