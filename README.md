# py-coreutils

A collection of python scripts to manage files. 

- `rmv3`: remove files made safe - It will send files to the trash by default, instead of delete the files.
- `recover.py`: it will bring a function to manage files in the trash, such as recover the file, list the files, etc.

## rmv3

usage: 
`rmv3 [-h] [-v] [-r] [-f] [-D] [--trash-dir DIR] FILE [FILE ...]`


positional arguments:
`FILE             files/dirs to be removed`

options:
```bash
-h, --help       show this help message and exit
-v, --verbose    show process on STDIN
-r, --recursive  execute command recursively
-f, --force      run action without asking for confirmation
-D, --delete     delete the files instead of sending them to TRASH
--trash-dir DIR  directory where the removed files will be moved
```

## recover

usage: 
`recover [-h] [-l | -r] [FILE ...]`

positional arguments:
`FILE              files/dirs to be removed`

options:

``` sh
-h, --help        show this help message and exit
-l, --list-files  look for FILE in trash dir - if not FILE is given it show all files
-r, --recover     take files from trash directory to working directory. This is the default value
```

