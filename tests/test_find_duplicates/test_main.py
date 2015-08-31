# -*- UTF-8 -*-

import pytest
from mock import patch

import find_duplicates


def test_main_parse_default_args():
    args = find_duplicates.parse_args([])
    assert args.scandir == '.'
    assert not args.verbose


def test_main_parse_args_ok():
    args = find_duplicates.parse_args(['--verbose', '/foo/bar'])
    assert args.verbose
    assert args.scandir == '/foo/bar'

