#!/usr/bin/env python
# -*- UTF8 -*-

import sys
import argparse
from .biz_func import *
from utils.verbose import Verboser

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
    return process_candidate_files(root_dir)


def format_duplicates(duplicates, outfile):
    for files in duplicates:
        for file in files:
            outfile.write( "# rm " + file + '\n')
        outfile.write("# --\n")


def parse_args(args=sys.argv):
    """ find duplicates main function"""
    parser = argparse.ArgumentParser(prog='find_duplicates', description="""
        Find duplicates in file system

        Scan a directory for duplicate files by checking name, size and md5.
        The output is written to stdout.
        - Each filename (full path) is written in one line
        - Set of identical file names is separated by a line containing '--'

        """)
    parser.add_argument('scandir', action='store', default='.',
                        help='Name of the directory to scan')
    parser.add_argument('--version',
                   help='Print the package version to stdout',
                   action='version', version='%(prog)s ' + __version__)

    parser.add_argument('-v', '--verbose', action='count', default=0,
                   help='print verbosity information (can be multiple given)')
    parser.add_argument('-o', '--outfile',
                        type=argparse.FileType('w'), default=sys.stdout,
                        help='Write output to file instead of stdout')

    return parser.parse_args(args)


def main():
    """ find duplicates main function"""
    args = parse_args(sys.argv[1:])
    Verboser().set_level(args.verbose)
    Verboser().verbose_min("Scandir {0}".format(args.scandir))
    duplicates = find_duplicates(args.scandir)
    sort_members(duplicates)
    duplicates = make_unique(duplicates)
    format_duplicates(duplicates, args.outfile)
    args.outfile.close()


if __name__ == "__main__":
    main()