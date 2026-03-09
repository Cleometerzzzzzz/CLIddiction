# CLIddiction
Command-Line addiction recovery tracker &amp; relapse timer

## Dependencies
python3

## How to Install
1.)
  Clone the Repo. You should now have the file main.py

2a.) 
  Use Pyinstaller to compile main.py into cliddiction, then move this to wherever your PATH is

2b.)
  Make a file with the content:
```
#! /usr/bin/env bash
python3 "$HOME/path/to/main.py" "$@"
```

and name it cliddiction. use `` chmod +x cliddiction `` to make it executable.
3b.)
  in ~/.bashrc, add this to the bottom of the file:
``
export PATH="$HOME/path/to/dir/containing/cliddiction:$PATH"
``


You can now call cliddiction from anywhere.

## How to Use
  usage: main.py [-h] [-n] [-r] [-c COMMENT]

options:
  -h, --help            show this help message and exit
  -n, --new             Create new tracker
  -r, --reset           Reset tracker
  -c COMMENT, --comment COMMENT
                        Note to add when resetting tracker
