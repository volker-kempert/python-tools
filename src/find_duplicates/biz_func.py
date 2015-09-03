# -*- UTF8 -*-

from os.path import basename, getsize
import hashlib
import os
from verbose import Verboser

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
    max_files = count_files(base_dir)
    complete_list = []
    file_no = 0
    old_percent = 0
    for directory, _, files in os.walk(base_dir):
        for file in files:
            full_name = os.path.join(directory, file)
            same_files = find_other_files(other_dir, full_name)
            if len(same_files) > 1:
                complete_list.append(same_files)
            file_no += 1
            new_percent = int(file_no * 100 / max_files)
            if old_percent < new_percent:
                Verboser().verbose_max("Progress {0} %".format(new_percent))
                old_percent = new_percent
    Verboser().verbose_max("Found duplicates: {0}".format(len(complete_list)))
    return complete_list


def find_other_files(base_dir, ref_file):
    """
    Find files of the same content as ref_file anywhere below base_dir

    :param base_dir (string): Name of the directory that is to be searched
    :param ref_file (string): Name of the reference file to be compared with
    :returns (list): Tuple of file names where files have the same content
        empty list if there is no duplicate found, otherwise ref_file will
        be placed into the list as well
    """
    Verboser.verbose_debug('Dir : {0}, Ref-file {1}'.format(base_dir, ref_file),
                           func=find_other_files.__name__)
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

def sort_members(items):
    Verboser().verbose("Sort Items")
    for item in items:
        item.sort()


def make_unique(original_list):
    Verboser().verbose("Remove duplicate items")
    unique_list = []
    map(lambda x: unique_list.append(x) if (x not in unique_list) 
                                        else False, original_list)
    Verboser().verbose_max("Reduced duplicates to {0}".format(len(unique_list)))
    return unique_list


def count_files(base_dir):
    """
    count the number of below base_dir

    :param base_dir (string): Name of the directory that is to be searched
    :returns (int): number of files
    """
    count = 0
    for directory, _, files in os.walk(base_dir):
        for file in files:
            count += 1
    return count


def handle_based_on_filter(duplicates, filter):
    """ Filter of all files that are located that have misc as part of dir

    :param duplicates (list of lists): contain duplicate file record)
    :param filter (function): Take recode return True/false if the filter applies
    :returns (tuple): of handled and not_handled sets
    """
    handled = []
    not_handled = []

    for record in duplicates:
        if filter(record):
            handled.append(record)
        else:
            not_handled.append(record)
    Verboser().verbose_max("Orig {2} Filtered misc {0} remainder {1}".format(
                            len(handled), len(not_handled), len(duplicates)))
    return (handled, not_handled)


def remove_misc(duplicates):
    """ Filter of all files that are located that have misc as part of dir
    :returns (tuple): of handled and not_handled sets
    """
    def filter(record):
        return 2 == len(record) and 'misc' in record[1]
    return handle_based_on_filter(duplicates, filter)


def remove_2014(duplicates):
    """ Filter of all files that are located that have 2014 as part of dir
    :returns (tuple): of handled and not_handled sets
    """
    def filter(record):
        return 2 == len(record) and '/2014/' in record[1]
    return handle_based_on_filter(duplicates, filter)
