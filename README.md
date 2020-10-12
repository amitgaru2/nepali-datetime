# Nepali Datetime (Bikram Sambat B.S & Nepal Time NPT) 

The package similar to Python's core ``datetime`` package that
operates on Bikram Sambat (B.S) date & Nepal Time ``+05:45``.

## Installation
```shell
$ pip install nepali-datetime
```

## Usage
The `Python3` core [``datetime``](https://docs.python.org/3.5/library/datetime.html) library usage _VS_ `nepali_datetime` usage.
```python
# importing the module
>>> import datetime
>>> import nepali_datetime

# getting today's date
>>> datetime.date.today()
>>> nepali_datetime.date.today()

# getting now datetime
>>> datetime.datetime.now()
>>> nepali_datetime.datetime.now()

# creating date object
>>> datetime.date(2020, 9, 4)
>>> nepali_datetime.date(2077, 5, 19)

# creating datetime object
>>> datetime.datetime(2020, 9, 4, 8, 26, 10, 123456)
>>> nepali_datetime.datetime(2077, 5, 19, 8, 26, 10, 123456)

# date/datetime formatting
>>> datetime.datetime(2020, 9, 4, 8, 26, 10, 123456).strftime("%d %B %Y") # 04 September 2020
>>> nepali_datetime.datetime(2077, 5, 19, 8, 26, 10, 123456).strftime("%d %B %Y") # 19 Bhadau 2077 
```

***Note**: The equivalence is not limited to just getting current datetime. Its 
supports most of the methods from Python's core datetime library. Check 
documentation for more details.

## Documentation
Complete documentations can be found [here](https://dxillar.github.io/nepali-datetime/).


## Contribution

For contribution check the guidelines in [CONTRIBUTING.md](https://github.com/dxillar/nepali-datetime/blob/master/CONTRIBUTING.md).
