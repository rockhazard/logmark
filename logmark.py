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
from pathlib import Path as p
from logmark_args import Arguments
from logmark_logic import CoreLogic
from logmark_gui import GUI

ROOT_DIR = p(__file__).parent
# icon_path = str(ROOT_DIR.joinpath('icons', 'logmark_light_icon_24x24.png'))
icon_path = 'icons/logmark_light_icon_24x24.png'
# icon_path = None


def main():
    """Allow user selection between cli and gui modes."""
    version_str = 'v0.1b "Chedder"'
    lm_logic = CoreLogic(_version=version_str)
    if len(sys.argv) == 1:
        gui = GUI(_version=version_str, logic=lm_logic, icon=icon_path)
        gui.main_loop()
    else:  # if any cli arguments, execute cli version of program
        cli_args = Arguments(_version=version_str)
        lm_logic.export_files(cli_args.args.INPUT_DIR, cli_args.args.OUTPUT_DIR,
                              cli_args.args.heading,
                              cli_args.args.prevent_duplicate_headings,
                              cli_args.args.tags)


if __name__ == '__main__':
    sys.exit(main())
