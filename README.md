# Nepali Datetime (Bikram Sambat B.S) 

The package similar to Python core ``datetime`` package that
operates on Bikram Sambat (B.S) date instead of A.D.

## Installation
```shell
$ pip install nepali-datetime
```

## Usage
The Python3 core `datetime` library usage.
```python
# Get current datetime in AD format
>>> import datetime
>>> datetime.datetime.now()
# 2020-07-18 12:18:53.586455
>>> datetime.date.today()
# 2020-07-18
```

The equivalent `nepali_datetime` library usage. 
```python
# Get current datetime in BS format
>>> import nepali_datetime
>>> nepali_datetime.datetime.now()
# 2077-04-03 12:18:53.586455
>>> nepali_datetime.date.today()
# 2077-04-03
```

**The equivalence is not limited to just getting current datetime. Its supports almost methods from Python's core 
datetime library supports & is almost equivalent. The ultimate goal is not make it equivalent & making these two 
library's interchangeable at any line of code.**

## Documentation
Complete documentations can be found [here](https://arneec.github.io/nepali-datetime/).


## Contribution

For contribution check the guidelines in [CONTRIBUTING.md](https://github.com/arneec/nepali-datetime/blob/master/CONTRIBUTING.md).
