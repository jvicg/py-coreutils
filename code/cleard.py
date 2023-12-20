#!/usr/bin/env python3

# py-coreutils/cleard.py
# script to remove old files automatically in a given dir

import os
import funcs
import globvars
from datetime import datetime

CHECKING_DIR = globvars.TRASH_DIR
NOW = datetime.now()
MIN_DAYS_TO_REMOVE = 7

files = funcs.get_dir_files(CHECKING_DIR)

for f in files:
    full_file_path = os.path.join(CHECKING_DIR, f)
    file_modify_time = datetime.fromtimestamp(os.path.getmtime(full_file_path))
    print((NOW - file_modify_time).days)
    if (NOW - file_modify_time).days > MIN_DAYS_TO_REMOVE: funcs.delete(full_file_path)
