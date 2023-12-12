#!/usr/bin/env python3

# py-coreutils/recover.py
# script to manage files in the TRASH

# TODO: make --recover the default flag

import os
import sys
import funcs                                  # file with local functions
import globvars                               # file that stores program global variables
import argparse

# program definition
PROG_NAME = "recover"
PROG_DEFINITION = f"{PROG_NAME} - program to manage files in the TRASH"
PROG_EPILOG = f"{globvars.PROJECT_NAME}/{PROG_NAME} - script part of the repo: {globvars.PROJECT_URL}"

def main():
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description=PROG_DEFINITION,
        epilog=PROG_EPILOG)

    # arguments - flags
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='show process on STDIN')

    # create exclusive group (so -r and -l can't be used together)
    exclusive_group = parser.add_mutually_exclusive_group()

    exclusive_group.add_argument(
        '-l', '--list-files',
        action='store_true',
        help='look for FILE in trash dir - if not FILE is given it show all files')

    exclusive_group.add_argument(
        '-r', '--recover',
        action='store_true',
        help='take files from trash directory to working directory. This is the default value')

    parser.add_argument(
        'files',
        nargs="*",
        default=["__show_all__"],
        metavar="FILE",
        help='files/dirs to be removed')

    args = parser.parse_args()                # args object (type: Namespace)
    recover: bool = args.recover              # recover mode
    list_files: bool = args.list_files        # list_files mode
    verbose: bool = args.verbose              # verbose mode
    files: list = args.files                  # files

    # execution of the program
    for f in files:
        if (not recover and not list_files) or recover:
            funcs.recover(globvars.TRASH_DIR, f, verbose)
        else:
            funcs.list_files(globvars.TRASH_DIR, f)

if __name__ == '__main__':
    main()
