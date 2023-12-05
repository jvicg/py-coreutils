# funcs.py
# file with funcs used in the rest of scripts

import os

# method to get size in MB of a given file
def get_filesize(f) -> int:
    return os.path.getsize(f)/(1024**2) # it will return the size in MB

# method to get the size in MB of a given dir
def get_dirsize(d) -> int:
    dir_size = 0
    for root, dirs, files in os.walk(d):
        for f in files:
            full_file_path = os.path.join(root, f)
            dir_size += get_filesize(full_file_path)
    return dir_size

# method to get the size of in MB of a dir or a file
def get_size(f) -> int:
    if os.path.isdir(f):
        return get_dirsize(f)
    elif os.path.isfile(f):
        return get_filesize(f)
