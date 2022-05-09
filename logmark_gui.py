#!/usr/bin/env python3

"""
GUI interface for logmark
License: GPL 3.0
Author: rockhazard
Date: 2022
"""
from subprocess import run, CalledProcessError
import logmark as lm
import PySimpleGUI as sg  # type: ignore
# import PySimpleGUIQt as sg  # type: ignore
# import PySimpleGUIWeb as sg  # type: ignore
# import PySimpleGUIWx as sg # type: ignore

version = lm.version()
# sg.SetIcon(icon=None)
# sg.theme('LightBlue3')
sg.theme('DarkGrey11')
sg.set_options(font='Roboto')

# tooltips
optional_text = 'Optional comma-separated list of tags to add to all files'
source_dir_tip = 'Please enter an absolute path.'
output_dir_tip = 'Please enter an absolute path with a trailing "/".'
layout = [
    # Row  1
    [sg.Text('Choose Heading Level'), sg.Spin([1, 2, 3, 4, 5, 6], pad=(4, 2),
                                              key='-HEADING-'),
        sg.Text('Suppress Duplicate Headings'),
        sg.Checkbox(text='', enable_events=True, key="-SUPPRESS_DUPES-")],
    # Row  2
    [sg.Text('Global Tag List'), sg.Input(key='-GLOBAL_TAGS-', border_width=0,
                                          expand_x=True, tooltip=optional_text)],
    # Row  3
    [sg.Text('Source Directory'), sg.Input(tooltip=source_dir_tip,
                                           key='-SOURCE_DIR-', expand_x=True,
                                           border_width=0)],
    # Row  4
    [sg.Text('Output Directory'), sg.Input(tooltip=output_dir_tip,
                                           key='-OUTPUT_DIR-', expand_x=True,
                                           border_width=0)],
    # Row  5
    [sg.Button('Export', key='-EXPORT-', expand_x=True, border_width=0),
     sg.Button('Help', key='-HELP-', expand_x=True, border_width=0),
     sg.Button('Cancel', key='-CANCEL-', expand_x=True, border_width=0)],
]


window = sg.Window(f'Logmark {version}', layout)

while True:
    event, values = window.read()

    if event == '-HELP-':
        try:
            run(['xdg-open', 'https://github.com/rockhazard/logmark'], check=True)
        except CalledProcessError:
            print(
                'No default browser found: please visit https://github.com/rockhazard/logmark for help.')

    if values['-GLOBAL_TAGS-']:
        global_tags = values['i-GLOBAL_TAGS-'].split(',')
    else:
        global_tags = []

    if event in (sg.WIN_CLOSED, '-CANCEL-'):
        break
    if event == '-EXPORT-':
        try:
            lm.export_files(values['-SOURCE_DIR-'], values['-OUTPUT_DIR-'],
                            values['-HEADING-'], values['-SUPPRESS_DUPES-'],
                            global_tags)
        except ValueError as error:
            print(error)
            # window['-RESULTS-'].update(error)
        else:
            print(f"files exported to {values['-OUTPUT_DIR-']}")
            break
window.close()
