"""
Tests for the key signature class
"""

import pytest
import itertools

from pyabc import Key


def every_possible_key():
    """
    Create a list of every possible key that a user might send to software
    for use in testing.

    returns:
        A list of most of the more likely user inputs for key signature.

    references:
        http://abcnotation.com/wiki/abc:standard:v2.1#kkey
    """
    # Base List of Keys @TODO Need to add sharps and flats
    keys = ['A','B', 'C', 'D', 'E', 'F', 'G', 'Bb', 'C#', 'Eb', 'F#', 'G#']

    # List of Modes in Sentence case
    modes = ['Ionian', 'Aeolian', 'Mixolydian', 'Dorian', 'Phrygian',
     	    'Lydian', 'Locrian', 'Major', 'Minor']

    # Append upper and lower case versions of the above
    modes += [mode.lower() for mode in modes] +\
             [mode.upper() for mode in modes]

    # Append truncated versions of the above
    modes += [mode[:3] for mode in modes] + ['m']

    return [str(x[0] + x[1]) for x in itertools.product(keys, modes)]


@pytest.mark.parametrize("key", every_possible_key())
def test_parse_key_basic(key):
    # Attempt to create key using key string provided.
    Key(name=key)
