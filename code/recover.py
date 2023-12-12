#!/usr/bin/env python3

# py-coreutils/recover.py
# script to manage files in the TRASH

import os
import argparse
from itertools import zip_longest
import error               # module with display error functions
import funcs               # module with local functions
import globvars            # module to store program global variables

# program definition
PROG_NAME = "recover"
PROG_DEFINITION = f"{PROG_NAME} - program to manage files in the TRASH"
PROG_EPILOG = f"{globvars.PROJECT_NAME}/{PROG_NAME} - script part of the repo: {globvars.PROJECT_URL}"
DEFAULT_FILE_VALUE = "__show_all__"           # used to list all files if no arguments are given

def main():
    parser = argparse.ArgumentParser(
        prog=PROG_NAME,
        description=PROG_DEFINITION,
        epilog=PROG_EPILOG)

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
        default=[DEFAULT_FILE_VALUE],
        metavar="FILE",
        help='files/dirs to be removed')

    # args variables
    args = parser.parse_args()                # args object (type: Namespace)
    recover_mode: bool = args.recover         # recover mode
    list_mode: bool = args.list_files         # list_files mode
    arg_files: list = args.files              # files

    # if no flag is given, recover mode will be use as default (recover -r)
    if not recover_mode and not list_mode: recover_mode=True
    # if no flag and no arguments are given, program will list files in the trash (recover -l)
    if recover_mode and arg_files[0] == DEFAULT_FILE_VALUE:
        list_mode=True
        recover_mode=False

    # check if trash dir is empty
    if len(os.listdir(globvars.TRASH_DIR)) == 0:
        print(f'{PROG_NAME}: info: TRASH DIR is empty')
        exit(0)

    # main program loop
    for File in arg_files:
        trash_files, trash_dirs = funcs.get_dir_files(globvars.TRASH_DIR, File)
        list_files, list_dirs, recover_files = [], [], []
        for f, d in zip_longest(trash_files, trash_dirs): # iterate over trash files
            # handle file naming
            file_name, date = f.rsplit(globvars.FIELD_SEPARATOR)                # split filename and date
            if d != None: dir_name, date = d.rsplit(globvars.FIELD_SEPARATOR)   # split dirname and date
            if File in file_name or File == DEFAULT_FILE_VALUE:
                if recover_mode:
                    trash_file = os.path.join(globvars.TRASH_DIR, f)
                    recover_files.append((trash_file, file_name))
                elif list_mode:
                    list_files.append((file_name, date))
                    if d != None: list_dirs.append((dir_name, date))
        # execution
        if recover_mode and len(recover_files) > 0:
            print(f'{PROG_NAME}: RECOVERING FILES FROM TRASH DIR ({globvars.TRASH_DIR}):')
            for trash_file, f in recover_files:
                funcs.move(trash_file, f, PROG_NAME)
                print(f"{PROG_NAME}: file --> '{f}' successfully recovered on working directory")
        elif list_mode and len(list_files) > 0:
            print(f'{PROG_NAME}: LISTING FILES IN TRASH DIR ({globvars.TRASH_DIR}):')
            for file_name, date in list_files: print(f"{PROG_NAME}: file --> '{file_name}' removed on {date}")
            for dir_name, date in list_dirs: print(f"{PROG_NAME}: directory --> '{dir_name}' removed on {date}")
        # return error if no File is present in trash dir
        else: error.file_not_found(PROG_NAME, File)

    exit(0)

if __name__ == '__main__':
    main()
