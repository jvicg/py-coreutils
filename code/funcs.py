# py-coreutils/funcs.py
# file with funcs used in the rest of scripts

import os
import subprocess

# methods to print usage
def print_mvv3_usage():
    print("USAGE: mvv3 --move | -m | --copy | -c SOURCE/s DESTINATION")

# methods to get the size given file (will assume valid files/dirs are passed)
def get_filesize(f) -> int:
    return os.path.getsize(f)/(1024**2) # convert bytes to megabytes

def get_dirsize(d) -> int:
    dir_size = 0
    for root, dirs, files in os.walk(d):
        for f in files:
            full_file_path = os.path.join(root, f)
            dir_size += get_filesize(full_file_path)
    return dir_size

def get_size(f) -> int:
    if os.path.isdir(f):
        return get_dirsize(f)
    elif os.path.isfile(f):
        return get_filesize(f)

# method to remove separator (/) from the end of a directory name and get basename instead of full path
def get_basename(f) -> str:
    return os.path.basename(f.rstrip(os.path.sep))

# method to run a command - handling possible errors
def run(command):
    try:
        subprocess.run(command, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("ERROR", e)
    except Exception as e:
        print("ERROR:", e)

# method to delete files
def delete(f, verbose=False):
    command = ["/bin/rm", "-rf"]
    run(command)
    if verbose: print(f"rmv3: deleting -> '{f}'")

# method to move files to trash
def to_trash(f, trash_path, verbose=False):
    os.rename(f, trash_path)
    if verbose: print(f"rmv3: moving '{f}' -> {trash_path}")
