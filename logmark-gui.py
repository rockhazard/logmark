#!/usr/bin/env python3

"""
GUI interface for logmark
License: GPL 3.0
Author: rockhazard
Date: 2022
"""
import logmark as lm
import PySimpleGUI as sg  # type: ignore
# import PySimpleGUIQt as sg  # type: ignore
# import PySimpleGUIWeb as sg  # type: ignore
# import PySimpleGUIWx as sg # type: ignore

# constants
miles = 0.624
lbs = 2.20462

# sg.theme('LightBlue3')
sg.theme('DarkGrey11')
sg.set_options(font='Roboto')
optional_text = 'Optional comma-separated list of tags to add to all files'
layout = [
    # Row  1
    [sg.Text('Choose Heading Level'), sg.Spin([1, 2, 3, 4, 5, 6], pad=(4, 2),
                                              key='-HEADING-'),
        sg.Text('Suppress Duplicate Headings'),
        sg.Checkbox(text='', key="-SUPPRESS_DUPES-")],
    # Row  2
    [sg.Text('Global Tag List'), sg.Input(key='-GLOBAL_TAGS-', border_width=0,
                                         expand_x=True, tooltip=optional_text)],
    # Row  3
    [sg.Text('Source Directory'), sg.Input(
        key='-SOURCE_DIR-', expand_x=True, border_width=0)],
    # Row  4
    [sg.Text('Output Directory'), sg.Input(
        key='-OUTPUT_DIR-', expand_x=True, border_width=0)],
    # Row  5
    [sg.Button('Export', key='-EXPORT-', expand_x=True, border_width=0),
     sg.Button('Reset', key='-RESET-', expand_x=True, border_width=0),
     sg.Button('Cancel', key='-CANCEL-', expand_x=True, border_width=0)],
    # Row  6 (for error reporting)
    # [sg.Text('Result', enable_events=True, key='-RESULT-')],
]

window = sg.Window('Logmark', layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, '-CANCEL-'):
        break
    if event == '-EXPORT-':
        try:
            pass
        except ValueError as error:
            print(error)
            # window['-RESULTS-'].update(error)
window.close()
