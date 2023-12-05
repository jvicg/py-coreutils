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
mode = "mv"                    # the mode selected by the user (will be set as "mv" by default)

# first argument must indicate if program have to copy or move
COPY_FLAGS = ["--copy", "-c"]
MOVE_FLAGS = ["--move", "-m"]

if sys.argv[1] in COPY_FLAGS:
    mv = ["/bin/cp"]
    rsync = ["/bin/rsync", "-av", "--progress"]
    mode = "cp"
elif sys.argv[1] in MOVE_FLAGS:
    mv = ["/bin/mv"]
    rsync = ["/bin/rsync", "-av", "--progress", "--remove-source-files"]
else:
    print("ERROR: an option must be specified")
    funcs.print_usage()
    sys.exit(1)

# handle the rest of arguments
for arg in sys.argv[2:-1]:
    # strings with the pattern '-*' will be considered as a flag
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
        funcs.print_usage()
        sys.exit(1)

# if last argument is not a directory, the program will assum that user wants to rename the file
# so we just use regular /bin/mv
destination = sys.argv[-1]
if not os.path.isdir(destination) and mode == "mv":
    rsync = mv

# commands
no_progress_bar_command = mv + [flag for flag in flags] + [source for source in sources] + [destination]
progress_bar_command = rsync + [flag for flag in flags] + [source for source in rsync_sources] + [destination]

# execute commands
if len(sources) != 0:
    funcs.run(no_progress_bar_command)
if len(rsync_sources) != 0:
    funcs.run(progress_bar_command)
