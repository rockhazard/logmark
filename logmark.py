#!/usr/bin/env python3


"""
Program: logmark
Description: Logmark tags markdown files using their directory structure as the
Logseq-style page reference notation (e.g. [[tag]]).
License: GPL 3.0
year: 2022
author: rockhazard
"""

import sys
from logmark_args import Arguments
from logmark_cli import CLI
from logmark_gui import GUI
# import argparse
# from textwrap import dedent
# from pathlib import Path as p
# from common import read_list, write_list


def main():

    if len(sys.argv) == 1:
        gui = GUI()
        gui.main_loop()
    else:
        lm_cli = CLI()
        args = Arguments()
        lm_cli.export_files(args.INPUT_DIR, args.OUTPUT_DIR, args.heading,
                            args.remove_duplicates, args.tags)


if __name__ == '__main__':
    sys.exit(main())
