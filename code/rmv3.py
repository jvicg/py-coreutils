#!/usr/bin/env python3

# py-coreutils/rmv3.py
# script to remove files or move them to TRASH

import os
import argparse
import subprocess
import datetime
import error               # module with display error functions
import funcs               # module with local functions
import globvars            # module to store program global variables

# handle file naming
now = datetime.datetime.now()                  # start clock
DATE = now.strftime("%c")                      # date as string
TRASH_FORMAT = globvars.FIELD_SEPARATOR+DATE   # TRASH extension (will be appended to the name of removed files)

# program definition
PROG_NAME = "rmv3"
PROG_DEFINITION = f"{PROG_NAME} - simple script to remove or move them to TRASH"
PROG_EPILOG = f"{globvars.PROJECT_NAME}/{PROG_NAME} - script part of the repo: {globvars.PROJECT_URL}"

def main():
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

    parser.add_argument(
        '--trash-dir',
        metavar='DIR',
        default=globvars.TRASH_DIR,
        help='directory where the removed files will be moved')

    # argument - files
    parser.add_argument(
        'files',
        nargs="+",
        metavar="FILE",
        help='files/dirs to be removed')

    # args variables
    args = parser.parse_args()              # arg object (type: Namespace)
    verbose: bool = args.verbose            # verbose flag
    recursive: bool = args.recursive        # recursive flag
    force: bool = args.force                # force flag
    delete: bool = args.delete              # delete flag
    trash_dir: str = args.trash_dir         # trash directory

    # process trash dir
    funcs.mkdir(trash_dir, PROG_NAME)

    # execution of the program
    for f in args.files:
        # check if args are valid files
        if os.path.isfile(f) or os.path.islink(f) or os.path.isdir(f):
            if os.path.isdir(f) and not recursive: error.is_dir(PROG_NAME, f) # throw an error if trying to remove a dir with no recursive flag
            if delete or os.path.islink(f): funcs.delete(f, PROG_NAME, verbose)
            else:
                f_basename = funcs.get_basename(f)
                destination = os.path.join(trash_dir, f_basename + TRASH_FORMAT)
                funcs.move(f, destination, PROG_NAME, verbose)
        # error handling
        else: error.not_valid_file(PROG_NAME, f)

    exit(0)    # stop execution with success exit code

if __name__=='__main__':
    main()
