#!/usr/bin/env python3

# py-coreutils/rmvv3.py
# script to replace rm - it will move files to a trash dir

import os
import argparse
import subprocess
from datetime import datetime

HOME = home_dir = os.path.expanduser('~')
TRASH_DIR = os.path.join(home_dir, ".trash")

# handle time to name trash files
now = datetime.now()
date = now.strftime("%d-%b-%Y-%T")

# create trash dir if didnt exists
if not os.path.isdir(TRASH_DIR):
    os.makedirs(TRASH_DIR)

# handle arguments
parser = argparse.ArgumentParser(description='rmv3 - program to move files to TRASH, instead of deleting')
parser.add_argument('-r', '--recursive', action='store_true', help='execute command recursively')
parser.add_argument('-f', '--force', action='store_true', help='force action')
parser.add_argument('document', nargs="+", help='files/dirs to be processed')
args = parser.parse_args()

# flags
recursive = args.recursive
force = args.force

for f in args.document:
    pass
