"""
command line application for NepaliDate
for help: `python -m nepali_date -h option`
i) display nepali date calendar on command line
        `python -m nepali_date calendar`

... more on docs
"""

import argparse

from nepali_date import NepaliDate


def show_calendar():
    NepaliDate.calendar()


def show_today_date():
    print(NepaliDate.today())


def show_current_month():
    print(NepaliDate.today().month)


def show_current_day():
    print(NepaliDate.today().day)


valid_options_map = {
    "calendar": show_calendar,
    "date": show_today_date,
    "month": show_current_month,
    "day": show_current_day
}

parser = argparse.ArgumentParser()
parser.add_argument(
    "option",
    help="valid options are `%s`" % ('` | `'.join(valid_options_map)),
)
args = parser.parse_args()

if args.option in valid_options_map:
    valid_options_map[args.option]()
