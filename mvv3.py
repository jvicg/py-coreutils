#!/usr/bin/env python3
# mvv3.py
# simple python script to execute mv or rsync depends on the file size
# it will show a progress bar when file size is greater than SIZE_FOR_PROGRESS_BAR (in MB)

import os
import sys
import funcs
import subprocess

# vars
SIZE_FOR_PROGRESS_BAR = 100    # minimum file size to show the progress bar
flags = []                     # list with all the given files by the user
sources = []                   # all the files or dirs that will be moved
rsync_sources = []             # same but with progress bar

# handle arguments

for arg in sys.argv[1:-1]:
    # string with the pattern '-*' will be considered as a flag
    if arg.startswith("-"):
        flags.append(arg)
    # check is args are files indeed
    elif os.path.isfile(arg) or os.path.isdir(arg):
        # check file size
        if funcs.get_size(arg) > SIZE_FOR_PROGRESS_BAR:
            rsync_sources.append(arg)
        else:
            sources.append(arg)
    else:
        print(f'ERROR: {arg} is not a valid file or directory')
        sys.exit(1)

# last arg must be a directory since is there where we are moving the files
if os.path.isdir(sys.argv[-1]):
    destination = sys.argv[-1]
else:
    print(f'ERROR: {sources[-1]} is not a directory')
    sys.exit(1)

# commands
mv_command = ["/bin/mv"] + [flag for flag in flags] + [source for source in sources] + [destination]
rsync_command = ["/bin/rsync", "--progress", "--remove-source-files"] + [flag for flag in flags] + [source for source in rsync_sources] + [destination]

# execute commands
if len(sources) != 0:
    subprocess.run(mv_command, capture_output=True, text=True, check=True)

if len(rsync_sources) != 0:
    subprocess.run(rsync_command, text=True, check=True)
