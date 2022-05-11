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


def main():
    VERSION = 'v0.1b "Chedder"'
    if len(sys.argv) == 1:
        gui = GUI(_version=VERSION)
        gui.main_loop()
    else:
        lm_cli = CLI(_version=VERSION)
        cli_args = Arguments(_version=VERSION)
        lm_cli.export_files(cli_args.args.INPUT_DIR, cli_args.args.OUTPUT_DIR,
                            cli_args.args.heading,
                            cli_args.args.remove_duplicates,
                            cli_args.args.tags)


if __name__ == '__main__':
    sys.exit(main())
