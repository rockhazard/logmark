#!/usr/bin/env python3

"""
GUI interface for logmark
License: GPL 3.0
Author: rockhazard
Date: 2022
"""
from subprocess import run, CalledProcessError
from pathlib import Path as p
from logmark_cli import CLI
# from version import VERSION
import PySimpleGUI as sg  # type: ignore
# import PySimpleGUIQt as sg  # type: ignore
# import PySimpleGUIWeb as sg  # type: ignore
# import PySimpleGUIWx as sg # type: ignore


class GUI:
    """CLI methods"""

    def __init__(self, **kwargs):  # classwide perams
        # User's home directory
        self.lm_cli = CLI()
        self._state = kwargs
        self.home = str(p.home())
        # tooltips
        self.optional_text = 'Optional comma-separated list of tags'
        self.source_dir_tip = 'Please enter an absolute path.'
        self.output_dir_tip = 'Please enter an absolute path.'

        # theme and style options
        sg.theme('DarkGrey11')
        sg.set_options(font='Roboto 16')
        # sg.SetIcon(icon=None)
        # sg.theme('LightBlue3')

        self.layout = [
            # Row  1
            [sg.Text('Choose Heading Level'), sg.Spin([1, 2, 3, 4, 5, 6],
                                                      pad=(4, 2),
                                                      key='-HEADING-'),
                sg.Text('Suppress Duplicate Headings'),
                sg.Checkbox(text='', enable_events=True,
                            key="-SUPPRESS_DUPES-")],
            # Row  2
            [sg.Text('Global Tag List'), sg.Input(key='-GLOBAL_TAGS-',
                                                  # border_width=0,
                                                  expand_x=True,
                                                  tooltip=self.optional_text)],
            # Row  3
            [sg.Text('Source Directory'), sg.Input(tooltip=self.source_dir_tip,
                                                   key='-SOURCE_DIR-',
                                                   expand_x=True,
                                                   # border_width=0
                                                   ),
                sg.FolderBrowse(button_text='Choose Source Directory',
                                initial_folder=self.home,
                                key='-PICK_SOURCE_DIR-')],
            # Row  4
            [sg.Text('Output Directory'), sg.Input(tooltip=self.output_dir_tip,
                                                   key='-OUTPUT_DIR-',
                                                   expand_x=True,
                                                   # border_width=0
                                                   ),
                sg.FolderBrowse(button_text='Choose Output Directory',
                                initial_folder=self.home,
                                key='-PICK_OUTPUT_DIR-')],
            [sg.Text('Status: ', key='-STATUS_LABEL-'),
             sg.Text('waiting to export', key='-STATUS-')],
            # Row  5
            [sg.Button('Export', key='-EXPORT-', expand_x=True,
                       # border_width=0
                       ),
             sg.Button('Help', key='-HELP-', expand_x=True,
                       # border_width=0
                       ),
             sg.Button('Exit', key='-EXIT-', expand_x=True,
                       # border_width=0
                       )],
        ]

    def main_loop(self):
        window = sg.Window(f'Logmark {self._state["_version"]}', self.layout)
        help = 'Please visit https://github.com/rockhazard/logmark for help.'
        while True:
            event, values = window.read()

            if event == '-HELP-':
                try:
                    run(['xdg-open', 'https://github.com/rockhazard/logmark'],
                        check=True)
                except CalledProcessError:
                    print(help)

            if values['-GLOBAL_TAGS-']:
                global_tags = values['-GLOBAL_TAGS-'].split(',')
            else:
                global_tags = []

            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break
            if event == '-EXPORT-':
                try:
                    self.lm_cli.export_files(values['-SOURCE_DIR-'],
                                             values['-OUTPUT_DIR-'],
                                             values['-HEADING-'],
                                             values['-SUPPRESS_DUPES-'],
                                             global_tags)
                except ValueError as error:
                    print(error)
                    window['-STATUS-'].update(error)
                else:
                    export_msg = f"files exported to {values['-OUTPUT_DIR-']}"
                    print(export_msg)
                    window['-STATUS-'].update(export_msg)
        window.close()
