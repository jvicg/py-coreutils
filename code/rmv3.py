#!/usr/bin/env python3

# py-coreutils/rmv3.py
# script to remove files or move files to TRASH

import os
import sys
import funcs                                  # file with local functions
import globvars                               # file that stores program global variables
import argparse
import subprocess
from datetime import datetime

# TODO: implement flag to change default TRASH_DIR

# handle file naming
now = datetime.now()                          # start clock
DATE = now.strftime("-%d-%b-%Y-%T")           # date as string
TRASH_FORMAT = DATE + globvars.TRASH          # add TRASH extension - format: {filename}-{date}.{TRASH}

# program definition
PROG_NAME = "rmv3"
PROG_DEFINITION = f"{PROG_NAME} - simple script to remove or move files to TRASH"
PROG_EPILOG = f"{globvars.PROJECT_NAME}/{PROG_NAME} - script part of the repo: {globvars.PROJECT_URL}"

parser = argparse.ArgumentParser(      # container for arguments specifications (object type: ArgumentParser)
    prog=PROG_NAME,
    description=PROG_DEFINITION,
    epilog=PROG_EPILOG)

# arguments - flags
parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    help='show process on STDIN')

parser.add_argument(
    '-r', '--recursive',
    action='store_true',
    help='execute command recursively')

parser.add_argument(
    '-f', '--force',
    action='store_true',
    help='run action without asking for confirmation')

parser.add_argument(
    '-D', '--delete',
    action='store_true',
    help='delete the files instead of sending them to TRASH')

# argument - files
parser.add_argument(
    'files',
    nargs="+",
    metavar="file",
    help='files/dirs to be removed')

args = parser.parse_args()              # arg object (type: Namespace)
verbose: bool = args.verbose            # verbose flag
recursive: bool = args.recursive        # recursive flag
force: bool = args.force                # force flag
delete: bool = args.delete              # delete flag

# create trash dir if doesn't exist
if not os.path.isdir(globvars.TRASH_DIR): os.makedirs(globvars.TRASH_DIR)

# execution of the program
for f in args.files:
    # files
    if os.path.isfile(f):
        if delete:
            funcs.delete(f, verbose)
        else:
            f_basename = funcs.get_basename(f)
            destination = os.path.join(globvars.TRASH_DIR, f_basename + TRASH_FORMAT)
            funcs.to_trash(f, destination, verbose)
    # dirs
    elif os.path.isdir(f):
        if not recursive:
            print(f'rmv3: error: {f} is a directory')
            sys.exit(1)
        elif not delete:
            dir_name = funcs.get_basename(f)
            destination = os.path.join(globvars.TRASH_DIR, dir_name + TRASH_FORMAT)
            funcs.to_trash(dir_name, destination, verbose)
        else:
            funcs.delete(f, verbose)
    # error handling
    else:
        print(f"rmv3: error: '{f}' is not a valid file or directory")
        sys.exit(1)

sys.exit(0)    # stop execution with success exit code
