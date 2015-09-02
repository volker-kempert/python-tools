# -*- UTF-8 -*-

import pytest
from mock import patch, Mock
import tempfile
import os

import find_duplicates.biz_func


@pytest.fixture
def file1(request):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write("test_content_file_1")
    f.close()
    def fin():
        os.remove(f.name)
    return f.name

@pytest.fixture
def file2(request):
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write("test_content_file_2")
    f.close()
    def fin():
        os.remove(f.name)
    return f.name


def test_compare_files_by_name(file1, file2):
    assert find_duplicates.biz_func.compare_files_by_name(file1, file1)
    assert not find_duplicates.biz_func.compare_files_by_name(file1, file2)


def test_compare_files_by_size(file1, file2):
    assert find_duplicates.biz_func.compare_files_by_size(file1, file1)
    assert find_duplicates.biz_func.compare_files_by_size(file1, file2)


def test_compare_files_by_md5(file1, file2):
    assert find_duplicates.biz_func.compare_files_by_md5(file1, file1)
    assert not find_duplicates.biz_func.compare_files_by_md5(file1, file2)


@patch("find_duplicates.biz_func.compare_files_by_name", return_value=True)
def test_compare_files_compose_name(compare_files_by_name, file1, file2):
    assert find_duplicates.biz_func.compare_files(file1, file2,
                        find_duplicates.biz_func.CHECK_NAME)
    assert compare_files_by_name.called_once_with(file1, file2)


@patch("find_duplicates.biz_func.compare_files_by_size", return_value=True)
def test_compare_files_compose_size(compare_files_by_size, file1, file2):
    assert find_duplicates.biz_func.compare_files(file1, file2,
                        find_duplicates.biz_func.CHECK_SIZE)
    assert compare_files_by_size.called_once_with(file1, file2)


@patch("find_duplicates.biz_func.compare_files_by_md5", return_value=True)
def test_compare_files_compose_md5(compare_files_by_md5, file1, file2):
    assert find_duplicates.biz_func.compare_files(file1, file2, 
                        find_duplicates.biz_func.CHECK_MD5)
    assert compare_files_by_md5.called_once_with(file1, file2)
