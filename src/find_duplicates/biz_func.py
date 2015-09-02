# -*- UTF8 -*-

from os.path import basename, getsize
import hashlib
import os
from utils.verbose import Verboser

# or-able flags
CHECK_NAME = 0x01
CHECK_SIZE = 0x02
CHECK_MD5 = 0x04


def compare_files_by_name(file1, file2):
    base1 = basename(file1)
    base2 = basename(file2)
    return base1 == base2


def compare_files_by_size(file1, file2):
    size1 = getsize(file1)
    size2 = getsize(file2)
    return size1 == size2


def compare_files_by_md5(file1, file2):
    md5_1 = hashlib.md5(open(file1, 'rb').read()).hexdigest()
    md5_2 = hashlib.md5(open(file2, 'rb').read()).hexdigest()
    return md5_1 == md5_2


def compare_files(file1, file2, mode):
    """ Compare two files following the and connection of various methods
    
    :param file1 (string): File name of the first file
    :param mode (integer): OR-ed set of Flags that indicate the methods
        CHECK_NAME, CHECK_SIZE and CHECK_MD5
    :return (Boolean): Value indicate if the files are the same
    """
    retval = True
    if mode & CHECK_NAME:
        retval = retval and compare_files_by_name(file1, file2)
    if mode & CHECK_SIZE:
        retval = retval and compare_files_by_size(file1, file2)
    if mode & CHECK_MD5:
        retval = retval and compare_files_by_md5(file1, file2)
    return retval


def process_candidate_files(base_dir, other_dir=None):
    """
    Recursively scan all files below scan_dir and follow up for 
    finding duplicates inside the same directory

    :param base_dir (string): Base directory name to search in 
    :param other_dir (string: Optional 2nd directory to search for duplicates
        if not given duplicates are searched in the very same base directory
    :return (list of lists): A collection of tuples of filenames addressing the
        same file content.
    """
    if not other_dir:
        other_dir = base_dir
    Verboser.verbose('Scan-candidate: base: {0} other: {1}'.format(
                                                    base_dir, other_dir))
    complete_list = []
    for directory, _, files in os.walk(base_dir):
        for file in files:
            full_name = os.path.join(directory, file)
            same_files = find_other_files(other_dir, full_name)
            if len(same_files) > 1:
                complete_list.append(same_files)
    return complete_list


def find_other_files(base_dir, ref_file):
    """
    Find files of the same conent as ref_file anywhere below base_dir

    :param base_dir (string): Name of the directory that is to be searched
    :param ref_file (string): Name of the reference file to be compared with
    :returns (list): Tuple of file names where files have the same content
        empty list if there is no duplicate found, otherwise ref_file will
        be placed into the list as well
    """
    Verboser.verbose_max('Find-other-files: Dir : {0}, Ref-file {1}'.format(
                                                    base_dir, ref_file))
    same_files = []
    for directory, _, files in os.walk(base_dir):
        for file in files:
            full_name = os.path.join(directory, file)
            if ref_file != full_name:
                if compare_files(ref_file, full_name,
                                 CHECK_NAME | CHECK_SIZE | CHECK_MD5):
                    same_files.append(full_name)
    if len(same_files) > 0:
        same_files.append(ref_file)
    return same_files

