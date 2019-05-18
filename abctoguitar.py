#!/usr/bin/env python3
# Convert simple ABC files into guitar notation.

import pyabc
import argparse

# Get Import args
parser = argparse.ArgumentParser(
    description="Take and ABC file and render possible guitar tabs")
parser.add_argument("input", type=str,
                    help="An ABC file to feed to this script.")
parser.add_argument("--maxfret", "-m",
                   type=int,
                   default=5,
                   help="The highest fret to allow use of. Default is 5th.")
args = parser.parse_args()

# Open input file
with open(args.input, 'r') as fhandle:
    RAW_TUNE=fhandle.read()

# Parse the tune using pyabc
try:
    tune = pyabc.Tune(RAW_TUNE)
except KeyError:
    tune = pyabc.Tune("X:0\n" + RAW_TUNE)



# Setup the Tuning
DADGAD = [pyabc.Pitch('D', -1),
          pyabc.Pitch('A', -1),
          pyabc.Pitch('D', 0),
          pyabc.Pitch('G', 0),
          pyabc.Pitch('A', 0),
          pyabc.Pitch('D', 1)]
DADGAD.reverse()

MAXFRET = args.maxfret


def setup_strings(tuning, maxfret, minfret):
    """
    Create a data structure representing all the playable notes

    Args:
        tuning (list of pyabc.Pitch):
            representing all the strings 0th fret note
        maxfret (int):
            the highest fret the guitarist is willing to use
        minfret (int):
            the lowest fret the guitarist is willing to use.
            @TODO -not yet implemented

    Returns:
        strings (dict):
            Nested dictionaries wit the form:
                {string: {fret: note_int}}
    """
    # For each string create a dictionary of {string: {fret: note}}
    strings = {}
    for i, string in enumerate(DADGAD):
        frets = {}
        for fret in range(minfret, maxfret):
            frets[fret + string.abs_value] =  fret
        strings[i + 1] = frets
    return strings

strings = setup_strings(DADGAD, MAXFRET, 0)
# Memoize this?
possible_tabs = []
for note in tune.tokens:
    if type(note) == pyabc.Beam:
        x = [note._text for i in range(6)]
        possible_tabs.append(x)
    elif type(note) != pyabc.Note:
        pass
    else:
        note.octave +=  -1
        options = []
        for gstring in strings.values():
            if note.pitch.abs_value in gstring.keys():
                options.append("{}".format(gstring[note.pitch.abs_value]))
            else:
                options.append("")

        possible_tabs.append(options)

import numpy as np
notation = np.array(possible_tabs).T
# print(notation)

str_outs = []
for line in notation:
    str_out = ''

    for i in line:
        if len(i) == 0:
            str_out += ("----")
        else:
            str_out += f"-{i:2s}-"


    bars = [bar for bar in str_out.split('|')]
    bargroups = []

    for i in range(0, len(bars), 4):
        bargroups.append('|' + '|'.join(bars[i: i+4]) + '|')

    str_outs.append(bargroups)


print(str(np.array(str_outs).T))
