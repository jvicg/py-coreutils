# pycoreutils/error.py
# module with function to display error information

def no_arguments(PROG_NAME):
    print(f'{PROG_NAME}: error: no arguments were given')
    exit(1)

def not_valid_file(PROG_NAME, File):
    print(f"{PROG_NAME}: error: '{File}' is not a valid file or directory")
    exit(2)

def is_dir(PROG_NAME, File):   # used when trying to delete a dir with no --recursive flag
    print(f'{PROG_NAME}: error: {File} is a directory')
    exit(3)

def file_not_found(PROG_NAME, File):
    print(f"{PROG_NAME}: error: file: '{File}' was not found at TRASH DIR")
    exit(4)

def no_option_specified(PROG_NAME):
    print(f'{PROG_NAME}: error an option must be specified')
    exit(5)
