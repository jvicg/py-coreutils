#!/usr/bin/env python3

# py-coreutils/recover.py
# script to manage files in the TRASH

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

    # args variables
    args = parser.parse_args()                # args object (type: Namespace)
    recover_mode: bool = args.recover         # recover mode
    list_mode: bool = args.list_files         # list_files mode
    verbose: bool = args.verbose              # verbose mode
    arg_files: list = args.files              # files

    if (not recover_mode and not list_mode): recover_mode = True # if no flag is given, recover mode will be use

    # execution of the program
    if len(os.listdir(globvars.TRASH_DIR)) == 0: # check if trash dir is empty
        print(f'{PROG_NAME}: ERROR: TRASH DIR is empty')
        sys.exit(1)

    # if user didn't give arguments in recover mode, returns error
    if recover_mode and arg_files[0] == '__show_all__':
        print(f'{PROG_NAME}: error: no arguments were given')
        sys.exit(1)

    # main script loop
    for File in arg_files:
        trash_files = funcs.get_dir_files(globvars.TRASH_DIR, File)
        list_files = []
        recover_files = []
        for f in trash_files: # iterate over trash files
            if File in f or File == '__show_all__':
                # handle file naming
                tmp = f.rsplit('.trash')[0]              # remove .trash extension
                file_name, date = tmp.rsplit('%_%')      # split filename and date
                # recover method
                if recover_mode:
                    trash_file = os.path.join(globvars.TRASH_DIR, f)
                    funcs.move(trash_file, file_name, PROG_NAME, True)
                    recover_files.append(file_name)
                # listing method
                elif list_mode:
                    list_files.append((file_name, date))     # append file to output list
        # if not present return error
        if (len(list_files) == 0 and list_mode) or (len(recover_files) == 0 and recover_mode):
            print(f"{PROG_NAME}: error: file: '{File}' was not found at TRASH DIR")
            sys.exit(1)
        else:
            for file_name, date in list_files:
                print(f"{PROG_NAME}: file: '{file_name}' removed at -> {date}")
    sys.exit(0)

if __name__ == '__main__':
    main()
