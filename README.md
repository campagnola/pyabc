# ABC to Guitar TAB Converter

Take an ABC tune and convert to guitar tab showing possible string/fret
combinations that will play the required note.

Current Command Line usage.

```
usage: abctoguitar.py [-h] [--output OUTPUT] [--maxfret MAXFRET]
                      [--minfret MINFRET] [--testmode]
                      input

Take and ABC file and render possible guitar tabs

positional arguments:
  input                 An ABC file to feed to this script.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Name for output file. If unset will replace *.abc with
                        *.tab
  --maxfret MAXFRET, -x MAXFRET
                        The highest fret to allow use of. Default is 5th.
  --minfret MINFRET, -m MINFRET
                        the lowest fret you wish to use. Default is 0.
  --testmode            turns on verbose printing out output

```

Tim Pillinger, 2019
based on the work of
Luke Campagnola, 2014
