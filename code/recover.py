#!/usr/bin/env python3

# py-coreutils/recover.py
# script to manage files in the TRASH

import os
import error                                  # module with display error functions
import funcs                                  # module with local functions
import globvars                               # module to store program global variables
import argparse

# program definition
PROG_NAME = "recover"
PROG_DEFINITION = f"{PROG_NAME} - program to manage files in the TRASH"
PROG_EPILOG = f"{globvars.PROJECT_NAME}/{PROG_NAME} - script part of the repo: {globvars.PROJECT_URL}"
DEFAULT_FILE_VALUE = "__show_all__"           # var will be used to list all files if no arguments are given

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

    if not recover_mode and not list_mode: recover_mode=True # if no flag is given, recover mode will be use as default

    # if user didn't give arguments in recover mode, returns error
    if recover_mode and arg_files[0] == DEFAULT_FILE_VALUE: error.no_arguments(PROG_NAME)

    # check if trash dir is empty
    if len(os.listdir(globvars.TRASH_DIR)) == 0:
        print(f'{PROG_NAME}: info: TRASH DIR is empty')
        exit(0)

    # main program loop
    for File in arg_files:
        trash_files = funcs.get_dir_files(globvars.TRASH_DIR, File)
        list_files, recover_files = [], []
        for f in trash_files: # iterate over trash files
            # handle file naming
            file_name, date = f.rsplit(globvars.FIELD_SEPARATOR)   # split filename and date
            if File in file_name or File == DEFAULT_FILE_VALUE:
                if recover_mode:
                    trash_file = os.path.join(globvars.TRASH_DIR, f)
                    recover_files.append((trash_file, file_name))
                elif list_mode:
                    list_files.append((file_name, date))
        # execution
        if recover_mode and len(recover_files) > 0:
            print(f'{PROG_NAME}: RECOVERING THE FILES:')
            for trash_file, f in recover_files: funcs.move(trash_file, f, PROG_NAME, True)
        elif list_mode and len(list_files) > 0:
            print(f'{PROG_NAME}: LISTING FILES IN THE TRASH:')
            for file_name, date in list_files:
                print(f"{PROG_NAME}: file --> '{file_name}' removed on {date}")
        # return error if no File is present in trash dir
        else: error.file_not_found(PROG_NAME, File)

    exit(0)

if __name__ == '__main__':
    main()
