#!/usr/bin/env python3


"""
Program: logmark
Description: Logmark tags markdown files using their directory structure as the
Logseq-style page reference notation (e.g. [[tag]]).
License: GPL 3.0
year: 2022
author: rockhazard
"""


import argparse
from textwrap import dedent


class Arguments:
    """CoreLogic arguments"""

    def __init__(self, **kwargs):
        self._state = kwargs

        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=dedent("""\
            Logmark tags markdown files using a file's parent directory names to
            create references. It uses Logseq's page reference notation to do this.
            For example, if you use '~/notes' as your source, Logmark would modify
            the file '~/notes/shopping/holiday/list.md' by inserting [[shopping]]
            and [[holiday]] tags with an optional heading 'list' at the top of the
            file 'list.md'. Logmark does not use the note collection's directory
            name or its parents as tags.

            """), epilog=dedent("""\
            Logmark is developed by rockhazard and licensed under GPL3.0. There are
            no warranties expressed or implied.
            """))
        self.required_args = self.parser.add_argument_group(
            'required arguments')
        self.required_args.add_argument('-i', '--INPUT_DIR', metavar='PATH',
                                        required=True,
                                        help='directory of the original files')
        self.required_args.add_argument('-o', '--OUTPUT_DIR', metavar='PATH',
                                        required=True,
                                        help='directory to place the \
                                        newly-tagged files')
        self.parser.add_argument('--version', help='print version info then exit',
                                 version=f'logmark {self._state["_version"]},\
                                 GPL3.0 © 2022, by rockhazard',
                                 action='version')
        self.parser.add_argument('-l', '--heading',
                                 help='write the filename (with no extension)\
                                 as the page heading with a numerical argument\
                                 for the heading level (e.g. "-l 3" writes\
                                 "### filename")', type=int,
                                 metavar='HEADING_LEVEL', default=1)
        self.parser.add_argument('-d', '--prevent_duplicate_headings',
                                 help='does not generate a heading from the\
                                 filename if it is already in the file',
                                 action='store_true')
        self.parser.add_argument('-t', '--tags',
                                 help='insert a list of tags at the top of\
                                 every fileafter the directory tags', type=str,
                                 nargs='+', default=None)
        self.args = self.parser.parse_args()
