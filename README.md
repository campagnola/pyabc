PyABC - Python package for parsing and analyzing ABC music notation
===================================================================

Luke Campagnola, 2014


Status:  Pre-alpha


Basic goals
-----------

* Be able to parse ABC tunes using most common formatting
* Analyze tunes to determine the modes and keys they use
* Automatically annotate tunes with chord names
* From a library of tunes, suggest sets that fit together nicely


Installation
------------
You can install pyabc as a module using
```bash
pip install -e /your/py/abc/directory
```

Testing
-------
Limit unit testing has been implemented. To run unit tests
```bash
cd /your/pyabc/directory
PYTHONPATH=$PYTHONPATH:$PWD pytest
```
