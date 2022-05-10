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
# import argparse
# from textwrap import dedent
from pathlib import Path as p
from common import read_list, write_list


# def version():
#     return 'v0.1b "Chedder"'

class CLI:
    """CLI methods"""

    def __init__(self, **kwargs):  # classwide perams
        # User's home directory
        self._state = kwargs
        self._state = dict(
            version='v0.1b "Chedder"',
        )

    def build_file_list(self, notebooks):
        files_list = []
        for file in p(notebooks).glob('**/*.md'):
            files_list.append(str(file))
        return files_list

    def build_tags(self, excluded_tags, md_file_path, write_heading=0, opt_tags=None):
        """excluded_tags excludes notes' parent dirs from tag list e.g. 'docs' in
        'docs/notes/file.md' will not become a tag in file.md)"""
        pages = []
        path_tags = p(md_file_path).parts
        for tag in path_tags[excluded_tags:-1]:
            pages.append(f'[[{tag}]]')
        if opt_tags:
            for tag in opt_tags:
                pages.append(f'[[{tag.strip()}]]')

        if write_heading > 6:
            sys.exit('operation not complete: heading level must be 6 or less')
        elif write_heading > 0:
            level = '#' * write_heading
            heading = f'{level} {p(md_file_path).stem} \n\n'
        else:
            heading = ''
        return '{}{}\n'.format(heading, ' '.join(pages))

    def export_files(self, input_dir, output_dir, heading, remove_duplicates, tags_list):
        """process the exporting of the provided files"""
        if not p(input_dir).exists():
            sys.exit('source path bad')
        if not p(output_dir).exists():
            sys.exit('destination path bad')
        # esnure files are exported inside named dir
        if not output_dir.endswith('/'):
            output_dir = str(p(output_dir).joinpath(' /')).rstrip()

        md_paths_list = self.build_file_list(input_dir)
        excluded_tags = len(p(input_dir).parts)
        for md in md_paths_list:
            insert_heading = heading
            md_file_lines = read_list(md)
            # prevent duplicate headings
            if remove_duplicates:
                # sometimes the filename is an existing heading in the file
                # in this case remove_duplicates will prevent repeated headings
                heading_dupe_test = '{} {}'.format('#' * heading, p(md).stem)
                if heading_dupe_test in md_file_lines[0:1]:
                    insert_heading = 0
            tags = self.build_tags(excluded_tags, md, insert_heading, tags_list)
            if insert_heading == 0 and '# ' in md_file_lines[0]:
                md_file_lines.insert(1, tags)
            else:
                md_file_lines.insert(0, tags)
            exported_file_name = output_dir + p(md).name
            write_list(exported_file_name, md_file_lines)


# def main():
#     """COMMANDLINE OPTIONS"""
#     pass
#
# if __name__ == '__main__':
#     sys.exit(main())
