"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""


from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyabc',  # Required
    version='1.0.0',  # Required
    description='A Python Library for Parsing ABC files',
    long_description=long_description,
    long_description_content_type='text/markdown',  # Optional (see note above)
    # @TODO url='https://github.com/pypa/sampleproject'
    author='Campagnola',
    python_requires='>3.6',
    # @TODO install_requires=['peppercorn'],
)
