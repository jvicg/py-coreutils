#!/usr/bin/env python3

# py-coreutils/mvv3.py
# simple python script to replace the commands /bin/mv and /bin/cp
# basically the script will execute rsync (which will show a progress bar) for big files
# and wil run the regular mv and cp for small files

# DEPENDENCIES: rsync
# USAGE: mvv3 OPTION SOURCE/s DESTINATION
#             OPTIONS: - move | m
#                      - copy | c

import os
import sys
import funcs
import subprocess

SIZE_FOR_PROGRESS_BAR = 100      # minimum megabytes to show the progress bar (this is intended to be modified)
flags = []                       # list with all the given flags by the user
destination = sys.argv[-1]       # destination always will be last argument passed by user
sources = []                     # all the files or dirs that will be moved
rsync_sources = []               # same but with progress bar

# no arguments given case
if len(sys.argv) < 3:
    print("ERROR: no arguments where given")
    funcs.print_mvv3_usage()
    sys.exit(1)

# process move/copy flag - must be the first argument (sys.argv[1])
COPY_FLAGS = ["--copy", "-c"]    # valid copy flags
MOVE_FLAGS = ["--move", "-m"]    # valid move flags
selected_mode = "mv"             # the mode selected by the user (will be set as "mv" by default)

if sys.argv[1] in COPY_FLAGS:
    mv = ["/bin/cp"]
    rsync = ["/bin/rsync", "-av", "--progress"]
    selected_mode = "cp"
elif sys.argv[1] in MOVE_FLAGS:
    mv = ["/bin/mv"]
    rsync = ["/bin/rsync", "-av", "--progress", "--remove-source-files"]
else:
    print("ERROR: an option must be specified")
    funcs.print_mvv3_usage()
    sys.exit(1)

# handle the rest of the arguments
for arg in sys.argv[2:-1]:
    # strings with the pattern '-*' will be considered as flags
    if arg.startswith("-"):
        flags.append(arg)
    # check is args are valid files/dirs
    elif os.path.isfile(arg) or os.path.isdir(arg):
        # check file size
        if funcs.get_size(arg) > SIZE_FOR_PROGRESS_BAR:
            rsync_sources.append(arg)
        else:
            sources.append(arg)
    # error handling
    else:
        print(f'ERROR: {arg} is not a valid file or directory')
        funcs.print_mvv3_usage()
        sys.exit(1)

# if last argument is not a directory, the program will assume that user wants to rename the file
# so we just use regular /bin/mv (no matter whats the file size)
if not os.path.isdir(destination) and selected_mode == "mv":
    rsync = mv

# commands composition
no_progress_bar_command = mv + [flag for flag in flags] + [source for source in sources] + [destination]
progress_bar_command = rsync + [flag for flag in flags] + [source for source in rsync_sources] + [destination]

# commands execution
if len(sources) != 0:
    funcs.run(no_progress_bar_command)
if len(rsync_sources) != 0:
    funcs.run(progress_bar_command)

sys.exit(0)
