#!/usr/bin/env python3
# py-coreutils/rmv3.py
# script to replace rm - it will move files to a trash dir

import os
import sys
import funcs
import argparse
import subprocess
from datetime import datetime

HOME_DIR = os.path.expanduser('~')
TRASH_DIR = os.path.join(HOME_DIR, ".trash")

# handle time to name trash files
now = datetime.now()
date = now.strftime("-%d-%b-%Y-%T") + ".trash"

# create trash dir if didnt exists
if not os.path.isdir(TRASH_DIR):
    os.makedirs(TRASH_DIR)

# handle arguments
parser = argparse.ArgumentParser(description='rmv3 - simple script to move files to TRASH')

# flags
parser.add_argument('-r', '--recursive',
                    action='store_true', help='execute command recursively')
parser.add_argument('-f', '--force',
                    action='store_true', help='run action without asking for confirmation')
parser.add_argument('--delete',
                    action='store_true', help='delete the files instead of sending them to TRASH')
# files
parser.add_argument('files',
                    nargs="+", metavar="file", help='files/dirs to be processed')

args = parser.parse_args()        # store arguments in a variable
recursive = args.recursive        # true if recursive flag was selected
force = args.force                # force flag
delete = args.delete              # delete flag

# execution of the program
for f in args.files:

    # files
    if os.path.isfile(f):
        if delete:
            funcs.delete(f)
        else:
            f_basename = funcs.get_basename(f)
            destination = os.path.join(TRASH_DIR, f_basename + date)
            funcs.to_trash(f, destination)
    # dirs
    elif os.path.isdir(f):
        if not recursive:
            print(f'rmv3: error: {f} is a directory')
            sys.exit(1)
        elif not delete:
            dir_name = funcs.get_basename(f)
            destination = os.path.join(TRASH_DIR, dir_name + date)
            funcs.to_trash(dir_name, destination)
        else:
            funcs.delete(f)
    # error handling
    else:
        print(f"rmv3: error: '{f}' is not a valid file or directory")
        sys.exit(1)

sys.exit(0)
