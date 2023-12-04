#!/usr/bin/env python3

import os
import sys
import subprocess

MIN_SIZE_FOR_RSYNC = 100

def get_file_size(f):
    return os.stat(f).st_size

# handle arguments
flags = []
sources = []
rsync_sources = []

for arg in sys.argv[1:]:

    # string with the pattern '-*' will be considered as a flag
    if arg.startswith("-"):
        flags.append(arg)

    # check is args are files indeed
    elif os.path.isfile(arg) or os.path.isdir(arg):
        sources.append(arg)
    else:
        print(f'ERROR: {arg} is not a valid file or directory')
        sys.exit(1)

if os.path.isdir(sources[-1]):
    destination = sources.pop(len(sources)-1)
else:
    print(f'ERROR: {sources[-1]} is not a directory')
    sys.exit(1)

# execute command
command = ["/bin/mv"] + [flag for flag in flags] + [source for source in sources] + [destination]

# try:
#     resultado = subprocess.run(command, capture_output=True, text=True, check=True)
# except subprocess.CalledProcessError as e:
#     print("ERROR:", e)
#     print("STDERR:", e.stderr)
# except Exception as e:
#     print("ERROR:", e)
