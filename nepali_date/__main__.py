"""
command line application for NepaliDate
for help: `python -m nepali_date -h option`
i) display nepali date calendar on command line
        `python -m nepali_date calendar`
"""

import argparse

from nepali_date import NepaliDate


def show_calendar():
    NepaliDate.calendar()


valid_options_map = {
    "calendar": show_calendar,
}

parser = argparse.ArgumentParser()
parser.add_argument("option", help='''
        valid options are `%s`
    ''' % ('` | `'.join(valid_options_map)), )
args = parser.parse_args()

if args.option in valid_options_map:
    valid_options_map[args.option]()
