# Nepali Datetime (Bikram Sambat Date & Nepal Time)

The package inspired from Python's core `datetime` package that
operates on top of Bikram Sambat (B.S) Date & Nepal Time (NPT) `+05:45`.

> Supports: **Python 3.5+**


## Basic Usage

```python
# importing
>>> import datetime
>>> import nepali_datetime

# today's date
>>> datetime.date.today()
>>> nepali_datetime.date.today()

# now datetime
>>> datetime.datetime.now()
>>> nepali_datetime.datetime.now()

# creating date object
>>> datetime.date(2020, 9, 4)
>>> nepali_datetime.date(2077, 5, 19)

# creating datetime object
>>> datetime.datetime(2020, 9, 4, 8, 26, 10, 123456)
>>> nepali_datetime.datetime(2077, 5, 19, 8, 26, 10, 123456)

# date/datetime formatting
>>> nepali_datetime.datetime(2077, 5, 19, 8, 26, 10, 123456).strftime("%d %B %Y")
# 19 Bhadau 2077

# datetime parsed from string (strptime)
>>> nepali_datetime.datetime.strptime('2077-09-12', '%Y-%m-%d')
# nepali_datetime.datetime(2077, 9, 12, 0, 0)

# date/datetime formatting with Nepali unicode support
>>> nepali_datetime.date(1977, 10, 25).strftime('%K-%n-%D (%k %N %G)')
# १९७७-१०-२५ (७७ माघ आइतबार)

# datetime.timedelta addition/subtraction
>>> nepali_datetime.date(1990, 5, 10) + datetime.timedelta(days=350)
# nepali_datetime.date(1991, 4, 26)
>>> nepali_datetime.datetime(1990, 5, 10, 5, 10, 20) + datetime.timedelta(hours=3, minutes=15)
# nepali_datetime.date(1990, 5, 10, 8, 25, 20)

# convert B.S to A.D date and vice-versa
>>> nepali_datetime.date(1999, 7, 25).to_datetime_date()
# datetime.date(1942, 11, 10)
>>> nepali_datetime.date.from_datetime_date(datetime.date(1942, 11, 10))
# nepali_datetime.date(1999, 7, 25)

# Bikram Sambat monthly calendar
>>> nepali_datetime.date(2078, 1, 1).calendar()

          Baishakh 2078
Sun  Mon  Tue  Wed  Thu  Fri  Sat
                1    2    3    4
5     6    7    8    9   10   11
12   13   14   15   16   17   18
19   20   21   22   23   24   25
26   27   28   29   30   31
```

## Installation

```shell
$ pip install nepali-datetime
```

## Documentation

Complete documentations is [here](https://amitgaru2.github.io/nepali-datetime/).

## Contribution

Any contributions are most welcome. Do check the guidelines in [CONTRIBUTING.md](https://github.com/amitgaru2/nepali-datetime/blob/master/CONTRIBUTING.md).
