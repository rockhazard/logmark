#!/usr/bin/env python3

"""
GUI interface for logmark
License: GPL 3.0
Author: rockhazard
Date: 2022
"""
from subprocess import run, CalledProcessError
from pathlib import Path as p
import PySimpleGUI as sg  # type: ignore
from logmark_logic import CoreLogic


class GUI:
    """Optional logmark gui."""

    def __init__(self, icon, logic=CoreLogic(), **kwargs):
        # User home directory
        self._state = kwargs
        self.logic = logic
        if not icon:
            self.title = False
            self.icon = None
        else:
            self.title = True
            self.icon = icon
        self.home = str(p.home())
        # tooltips
        self.optional_text = 'optional comma-separated list of tags to insert in all notes'
        self.source_dir_tip = 'Please enter an absolute path.'
        self.output_dir_tip = 'Please enter an absolute path.'

        # theme and style options
        sg.theme('DarkGrey11')
        # sg.theme('SystemDefaultForReal')
        sg.set_options(font='Roboto 16')
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
                                                  border_width=0,
                                                  expand_x=True,
                                                  tooltip=self.optional_text)],
            # Row  3
            [sg.Text('Notes Source Directory'), sg.Input(tooltip=self.source_dir_tip,
                                                         key='-SOURCE_DIR-',
                                                         expand_x=True,
                                                         border_width=0
                                                         ),
                sg.FolderBrowse(button_text='Choose Source Directory',
                                initial_folder=self.home,
                                key='-PICK_SOURCE_DIR-')],
            # Row  4
            [sg.Text('Notes Output Directory'), sg.Input(tooltip=self.output_dir_tip,
                                                         key='-OUTPUT_DIR-',
                                                         expand_x=True,
                                                         border_width=0
                                                         ),
                sg.FolderBrowse(button_text='Choose Output Directory',
                                initial_folder=self.home,
                                key='-PICK_OUTPUT_DIR-')],
            # Row  5
            [sg.Button('Export', key='-EXPORT-',
                       expand_x=True,
                       border_width=0
                       ),
             sg.Button('Help', key='-HELP-',
                       expand_x=True,
                       border_width=0
                       ),
             sg.Button('Exit', key='-EXIT-',
                       expand_x=True,
                       border_width=0
                       )],
            # Row 6
            [sg.Text('Status:  waiting to export',
                     expand_x=True,
                     background_color='black', key='-STATUS-')],

            # StatusBar won't update to display -OUTPUT_DIR- value
            # [sg.StatusBar('Status: waiting to export', relief='solid',
            #               enable_events=True, p=2, background_color='black',
            #               key='-STATUS-')],
        ]

    def main_loop(self):
        """load gui"""
        print(self.icon)
        window = sg.Window(f'Logmark {self._state["_version"]}', self.layout,
                           use_custom_titlebar=self.title, titlebar_icon=self.icon)
        help = 'Please visit https://github.com/rockhazard/logmark for help.'
        window.set_icon(icon='icon.png')
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
                    self.logic.export_files(values['-SOURCE_DIR-'],
                                            values['-OUTPUT_DIR-'],
                                            values['-HEADING-'],
                                            values['-SUPPRESS_DUPES-'],
                                            global_tags)
                except ValueError as error:
                    print(error)
                    window['-STATUS-'].update(f'Status: {error}')
                else:
                    export_msg = "Status: files exported to {}".format(
                        values['-OUTPUT_DIR-'])
                    print(export_msg)
                    window['-STATUS-'].update(export_msg)
        window.close()
