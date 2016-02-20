"""

"""
import os
import glob

from anchorhub.compatibility import get_path_separator
from anchorhub.util.addsuffix import add_suffix


def get_files(dir, exts, exclude=None, recursive=False):
    """
    Get a list of files within a directory with given extensions.
    Exclude/black list directories from the list if specified. By default,
    the search is recursive, looking in all subdirectories of 'dir'

    :param dir: String root directory to search under. All subdirectories are
        also searched by default
    :param exts: List of string file extensions. Files inside of dir with
        names ending with this string will be included in the list. Note: the
        string does not strictly need to be a file extension (beginging with
        a '.' dot), it could be the entire name of the file, or a common
        suffix to files.
    :param exclude: List of strings specifying directories that should not be
        included in the output list
    :param recursive: When True, search in all subdirectories, otherwise just
        look in the current directory
    :return: List of string directories
    """
    file_paths =[]
    if recursive:
        for root, _, _ in os.walk(dir):
            # os.walk() does not add path separator by default to end of path
            root = add_suffix(root, get_path_separator())
            if exclude is not None and is_dir_inside(root, exclude):
                # Skip directories that are in the exclude list
                continue
            file_paths.extend(get_files_in_dir(root, *exts))
    else:
        file_paths.extend(get_files_in_dir(dir, *exts))
    return file_paths


def get_files_in_dir(dir, *exts):
    """
    Creates a list of files in a directory that have the provided extensions.

    :param dir: String path of directory containing files to be listed
    :param exts: Variable amount of string arguments specifying the
        extensions to be used. If none are provided, will default to finding
        every file in the directory
    :return: A list of string paths to each desired file in the directory.
    """
    file_paths = []
    if exts is None:
        exts = ['']
    for ext in exts:
        file_paths.extend(glob.glob(dir + '*' + ext))
    return file_paths


def is_dir_inside(dir, check_dirs):
    """
    Check to see if dir is a subdirectory of (or matches) check_dir
    directories. Return True if the dir is a subdirectory of or matches any of
    the check directories.

    :param dir: String path of directory that may or may not be a
        subdirectory of or match the directories listed in check_dirs.
    :param check_dirs: List of string paths of directories that may be parents
        of dir
    :return: True if dir is a child/matches any of the directories in check.
        False otherwise
    """
    for check_dir in check_dirs:
        if os.path.commonprefix([dir, check_dir]) == check_dir:
            return True
    return False
