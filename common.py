#!/usr/bin/env python3

"""This is a collection frequently-used methods."""

__author__ = "rockhazard"
__copyright__ = "Copyright 2020, rockhazard"
__license__ = "MIT"
__version__ = "v0.1 beta"


def read_list(file):
    """Read given text file into a list."""
    with open(file, encoding='utf-8') as f:
        flist = f.read().splitlines()
    return flist


def write_list(new_file_name, source_list):
    """Write a list into a newline-seperated text file."""
    with open(new_file_name, 'w', encoding='utf-8') as output:
        for line in source_list:
            print(line, file=output, end='\n')
