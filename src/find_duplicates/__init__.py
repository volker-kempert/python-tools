#!/usr/bin/env python
# -*- UTF8 -*-

import sys
import argparse

try:
    from _version import __version__
except ImportError:
    __version__ = '--development-instance--'


def find_duplicates(root_dir):
    """
    find_duplicates identifies duplicate files below a directory

    :param root_dir (string): path describing the directory where duplicate
        files shall be searched for
    :returns (list): containing lists of strings with file names (full path)
    """
    return [['foo', 'bar']]


def parse_args(args=sys.argv):
    """ find duplicates main function"""
    parser = argparse.ArgumentParser(prog='find_duplicates', description="""
        Find duplicates in file system

        Scan a directory for duplicate files by checking name, size and md5
        The output is written to stdout.
        - Each filename (full path) is written in one line
        - Set of identical file names is separated by a line containing '--'

        """)
    parser.add_argument('--version',
                   help='Print the package version to stdout',
                   action='version', version='%(prog)s ' + __version__)

    parser.add_argument('-v', '--verbose', action='store_true',
                   help='print verbosity information')
    parser.add_argument('scandir', nargs='?', default='.',
                   help='Name of the directory to scan')
    return parser.parse_args(args)


def main(args=sys.argv):
    """ find duplicates main function"""
    args = parse_args(args)
    duplicates = find_duplicates(args.scandir)

if __name__ == "__main__":
    main()