# py-coreutils/globvars.py
# file with variables used in the scripts

import os

PROJECT_NAME = "pycoreutils"                       # project name
PROJECT_URL = "github.com/nrk19/py-coreutils"      # github repository
HOME_DIR = os.path.expanduser('~')                 # home directory
TRASH = ".trash"                                   # name of the trash directory (modify if u wish)
TRASH_DIR = os.path.join(HOME_DIR, TRASH)          # trash path
