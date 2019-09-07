from typing import List as _List, Union as _Union
import os as _os
import re as _re
import pathlib as _pathlib


def list_files(folder: str,
               name_pattern: str='.*',
               suffix: str=None) -> _List[str]:
    """List files within the given folder that satisfies the provided pattern.

    Args:
        folder: Folder for file searching.
        name_pattern: A regular expression for file name matching (excluding suffix).
        suffix: File suffix to be matched; or None if any suffix is acceptable.

    Returns:
        A sorted list of file names (can be empty).

    Raises:
        ValueError: If folder is not a valid system directory.
    """
    path = _pathlib.Path(folder)
    if path.is_dir():
        file_list = []
        general_pattern = _re.compile(name_pattern + '.*')
        if suffix is None:
            for file in path.glob('*'):
                filename = file.name
                if general_pattern.match(filename) and ('.' in filename or file.is_file()):
                    file_list.append(filename)
        else:
            for file in path.glob('*.' + suffix):
                file = file.name
                if general_pattern.match(file):
                    file_list.append(file)
        return sorted(file_list)
    else:
        raise ValueError('folder must be a valid path for a system directory.')
        

def list_folders(folder: str) -> _List[str]:
    """List all sub-folders within a given folder.

    Args:
        folder: Folder for sub-folder search.

    Returns:
        A sorted list of sub-folder names (can be empty).

    Raises:
        ValueError: If folder is not a valid system directory.
    """
    path = _pathlib.Path(folder)
    if path.is_dir():
        return sorted([folder.name for folder in path.glob('*') if '.' not in folder.name and folder.is_dir()])
    else:
        raise ValueError('folder must be a valid path for a system directory.')
    

def get_latest_file(folder: str,
                    name_pattern: str='.*',
                    suffix: str=None,
                    use_modified_time: bool=False) -> _Union[str, None]:
    """Get name of the latest file within the given folder that satisfies the provided pattern.

    Args:
        folder: Folder for file searching.
        name_pattern: A regular expression for file name matching (excluding suffix).
        suffix: File suffix to be matched; or None if any suffix is acceptable.
        use_modified_time: True if modified time is used for ranking and locating latest file;
            or False if creation time is used for ranking and locating latest file.

    Returns:
        Name of latest file; can be None if there is no file in the folder.

    Raises:
        ValueError: If folder is not a valid system directory.
    """
    path = _pathlib.Path(folder)
    if use_modified_time:
        time_func = _os.path.getmtime
    else:
        time_func = _os.path.getctime
    if path.is_dir():
        file_list = []
        time_list = []
        general_pattern = _re.compile(name_pattern + '.*')
        if suffix is None:
            for file in path.glob('*'):
                filename = file.name
                if general_pattern.match(filename) and ('.' in filename or file.is_file()):
                    file_list.append(file)
                    time_list.append(time_func(file))
        else:
            for file in path.glob('*.' + suffix):
                if general_pattern.match(file.name):
                    file_list.append(file)
                    time_list.append(time_func(file))
        if file_list:
            return file_list[max(range(len(time_list)), key=lambda i: time_list[i])].name
        else:
            return None
    else:
        raise ValueError('folder must be a valid path for a system directory.')
