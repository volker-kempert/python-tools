#!/usr/bin/env python
# -*- UTF8 -*-

import sys
import argparse
from verbose import Verboser
from find_duplicates.io import format_duplicates, \
    format_duplicates_with_remove, read_duplicates
from .biz_func import remove_misc, remove_2014

try:
    from _version import __version__
except ImportError:
    __version__ = '--development-instance--'





def parse_args(args=sys.argv):
    """ find duplicates main function"""
    parser = argparse.ArgumentParser(prog='find_duplicates', description="""
        Find duplicates in file system

        Scan a directory for duplicate files by checking name, size and md5.
        The output is written to stdout.
        - Each filename (full path) is written in one line
        - Set of identical file names is separated by a line containing '--'

        """)

    parser.add_argument('--version',
                   help='Print the package version to stdout',
                   action='version', version='%(prog)s ' + __version__)

    parser.add_argument('-v', '--verbose', action='count', default=0,
                   help='print verbosity information (can be multiple given)')
    parser.add_argument('-o', '--outfile',
                        type=argparse.FileType('w'), default=sys.stdout,
                        help='Write remaining output to file instead of stdout')
    parser.add_argument('-i', '--infile',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='Read from file, instaed of stdin')

    parser.add_argument('--filtermisc',
                        action='store_true', default=False,
                        help='Remove misc duplicates commands at rm-misc.sh')

    parser.add_argument('--filter2014',
                        action='store_true', default=False,
                        help='Remove 2014 duplicates commands at rm-misc.sh')

    return parser.parse_args(args)


def main():
    """ find duplicates main function"""
    args = parse_args(sys.argv[1:])
    Verboser().set_level(args.verbose)
    Verboser().verbose_min("Filter duplicates")
    duplicates = read_duplicates(args.infile)
    if args.filtermisc:
        handled, duplicates = remove_misc(duplicates)
        with open('rm-misc.sh', 'w') as fp:
            format_duplicates_with_remove(handled, fp)
    if args.filter2014:
        handled, duplicates = remove_2014(duplicates)
        with open('rm-2014.sh', 'w') as fp:
            format_duplicates_with_remove(handled, fp)
    format_duplicates(duplicates, args.outfile)
    args.outfile.close()


if __name__ == "__main__":
    main()
