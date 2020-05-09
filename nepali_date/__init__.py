"""
The package for NepaliDate system i.e Bikram Sambat (BS) for various purposes like:
i) AD to BS date conversions and vice - versa.
ii) BS date today.
iii) timedelta addition/subtraction to BS date.
iv) Beautiful Nepali calendar in the terminal with justify option.
"""
from .date import NepaliDate

__version__ = "2.0.5"

__all__ = [
    'NepaliDate'
]
