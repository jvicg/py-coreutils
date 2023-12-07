#!/usr/bin/env python3

# py-coreutils/rmv3.py
# script to remove files or move files to TRASH

import os
import sys
import funcs
import argparse
import subprocess
from datetime import datetime

HOME_DIR = os.path.expanduser('~')            # home directory
TRASH = ".trash"                              # name of the trash directory (modify if u wish)
TRASH_DIR = os.path.join(HOME_DIR, TRASH)     # trash path

# handle file naming
now = datetime.now()                          # start clock
DATE = now.strftime("-%d-%b-%Y-%T")           # date as string
TRASH_FORMAT = DATE + TRASH                   # add TRASH extension - format: {filename}-{date}.{TRASH}

# create trash dir if dont exists
if not os.path.isdir(TRASH_DIR): os.makedirs(TRASH_DIR)

# program definition
parser = argparse.ArgumentParser(
    prog="rmv3",
    description='rmv3 - simple script to remove or move files to TRASH',
    epilog = "py-coreutils/rmv3 - script part of the repo: github.com/nrk19/py-coreutils")

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

args = parser.parse_args()        # arg object
verbose = args.verbose            # verbose
recursive = args.recursive        # true if recursive flag was selected
force = args.force                # force flag
delete = args.delete              # delete flag

# execution of the program
for f in args.files:
    # files
    if os.path.isfile(f):
        if delete:
            funcs.delete(f, verbose)
        else:
            f_basename = funcs.get_basename(f)
            destination = os.path.join(TRASH_DIR, f_basename + TRASH_FORMAT)
            funcs.to_trash(f, destination, verbose)
    # dirs
    elif os.path.isdir(f):
        if not recursive:
            print(f'rmv3: error: {f} is a directory')
            sys.exit(1)
        elif not delete:
            dir_name = funcs.get_basename(f)
            destination = os.path.join(TRASH_DIR, dir_name + TRASH_FORMAT)
            funcs.to_trash(dir_name, destination, verbose)
        else:
            funcs.delete(f, verbose)
    # error handling
    else:
        print(f"rmv3: error: '{f}' is not a valid file or directory")
        sys.exit(1)

sys.exit(0)
