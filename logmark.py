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
import argparse
from textwrap import dedent
from pathlib import Path as p
from common import read_list, write_list


def build_file_list(notebooks):
    files_list = []
    for file in p(notebooks).glob('**/*.md'):
        files_list.append(str(file))
    return files_list


def build_tags(excluded_tags, md_file_path, write_heading=0, opt_tags=None):
    # excluded_tags excludes notes' parent dirs from tag list
    # (e.g. 'docs' in 'docs/notes/file.md' will not become a tag in file.md)
    pages = []
    path_tags = p(md_file_path).parts
    for tag in path_tags[excluded_tags:-1]:
        pages.append(f'[[{tag}]]')
    if opt_tags:
        for tag in opt_tags:
            pages.append(f'[[{tag}]]')

    if write_heading > 6:
        sys.exit('operation not complete: heading level must be 6 or less')
    elif write_heading > 0:
        level = '#' * write_heading
        heading = f'{level} {p(md_file_path).stem} \n\n'
    else:
        heading = ''
    return '{}{}\n'.format(heading, ' '.join(pages))


def main():
    """
    COMMANDLINE OPTIONS
    """
    parser = argparse.ArgumentParser(
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
    parser.add_argument('INPUT_DIR',
                        help='directory of the original files')
    parser.add_argument('OUTPUT_DIR',
                        help='directory to place the newly-tagged files \
                        (use trailing slash)')
    parser.add_argument('-l', '--heading',
                        help='write the filename (with no extension) as the page\
                         heading with a numerical argument for the heading level \
                         (e.g. "-l 3" writes "### filename")', type=int,
                        metavar='HEADING_LEVEL', default=0)
    parser.add_argument('-t', '--tags',
                        help='insert a list of tags at the top of every file \
                        after the directory tags', type=str, nargs='+',
                        default=None)
    parser.add_argument('-d', '--remove_duplicates',
                        help='prevent duplicating headings', action='store_true')
    parser.add_argument('--version', help='print version info then exit',
                        version='logmark v0.1 "Chedder" beta, GPL3.0 © 2022, by rockhazard',
                        action='version')
    args = parser.parse_args()

    if not p(args.INPUT_DIR).exists():
        sys.exit('source path bad')
    if not p(args.OUTPUT_DIR).exists():
        sys.exit('destination path bad')

    md_paths_list = build_file_list(args.INPUT_DIR)
    excluded_tags = len(p(args.INPUT_DIR).parts)
    for md in md_paths_list:
        insert_heading = args.heading
        md_file_lines = read_list(md)
        # prevent duplicate headings
        if args.remove_duplicates:
            # sometimes the filename is an existing heading in the file
            # in this case remove_duplicates will prevent repeated headings
            heading_dupe_test = '{} {}'.format('#' * args.heading, p(md).stem)
            if heading_dupe_test in md_file_lines[0:1]:
                insert_heading = 0
        tags = build_tags(excluded_tags, md, insert_heading, args.tags)
        if insert_heading == 0 and '# ' in md_file_lines[0]:
            md_file_lines.insert(1, tags)
        else:
            md_file_lines.insert(0, tags)
        exported_file_name = args.OUTPUT_DIR + p(md).name
        write_list(exported_file_name, md_file_lines)


if __name__ == '__main__':
    sys.exit(main())
