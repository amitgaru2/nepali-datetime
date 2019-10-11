# Nepali Date (Bikram Sambat B.S) API 

The API similar to datetime.date() that works on the BS date instead of AD.
**Now with NEPALI language support for date display.**

### Installation
---
 
You can install the Nepali Date from PyPI: ```pip install nepali-date```


### Usage
---

**B.S Date today**
```python
from nepali_date import NepaliDate

print(NepaliDate.today())
print(NepaliDate.today(lang='nep'))   # for date in nepali language format
```

**Creating NepaliDate object (instance)**
```python
from nepali_date import NepaliDate
        
new_year_2050 = NepaliDate(2050, 1, 1)
new_year_2051 = NepaliDate('2051', '1', '1')

print(new_year_2050, new_year_2051)

# for date in nepali language
new_year_2052 = NepaliDate(2052, 1, 1, lang='nep')
new_year_2053 = NepaliDate('2053', '1', '1', lang='nep')

print(new_year_2052, new_year_2053)
```
**Adding/Subtracting datetime.timedelta to NepaliDate instance**
```python 
import datetime

from nepali_date import NepaliDate

new_year_2051 = NepaliDate(2051, 1, 1)
hundred_days_after_new_year_2051 = new_year_2051 + datetime.timedelta(days=100)
hundred_days_before_new_year_2051 = new_year_2051 - datetime.timedelta(days=100)
```
**Converting datetime.date to NepaliDate or vice-versa**
```python
import datetime

from nepali_date import NepaliDate

my_birthday_in_ad = datetime.date(1995, 10, 15)
my_birthday_in_bs = NepaliDate.to_nepali_date(my_birthday_in_ad)

my_birthday = NepaliDate(2051, 10, 1)
my_birthday_in_ad = my_birthday.to_english_date()
```
### Monthly Calendar
---
**Current nepali month calendar highlighting today's date**
```python
from nepali_date import NepaliDate
NepaliDate.calendar()
```
![Screenshot](https://raw.githubusercontent.com/arneec/nepali-date/master/screenshots/nepali_monthly_calendar.PNG)


### Date in iso-format ie. 'YYYY-MM-DD'
---
```python
dt = NepaliDate(2076, 4, 2)
print(dt.isoformat())

dt_nep = NepaliDate(2076, 6, 24, lang='nep')
print(dt_nep.isoformat())   # २०७६-०६-२४
```

### Date display formatting
---
Format Specifier | Meaning | Example
--- | --- | ---
```%d``` | Day of the month as a zero-padded decimal number. | 01, 02, ..., 32
```%b``` | Month as abbreviated name. | Bai, Jes, ..., Cha
```%B``` | Month as full name. | Baishak, Jestha, ..., Chait
```%m``` | Month as a zero-padded decimal number. | 01, 02, ..., 12
```%y``` | Year without century as a zero-padded decimal number. | 00, 01, ..., 99
```%Y``` | Year with century as a decimal number. | 0001, 0002, ..., 2075, 2076, ..., 9999

```python
dt = NepaliDate(2076, 4, 7)
print("{0:B} {0:d}".format(dt))
```

### strfdate
---
Similar API to ```datetime.datetime.strftime```. NepaliDate to formatted string. Follow the formatting table to know the formatting string.
```python
dt = NepaliDate(2075, 10, 10)
print(dt.strfdate('%Y/%m/%d'))

dt_nep = NepaliDate(2076, 6, 24)
print(dt_nep.strfdate('%Y/%m/%d'))   # २०७६/०६/२४
```

### strpdate
---
Similar API to ```datetime.datetime.strptime```. Return NepaliDate instance if string and format matches. Follow the formatting table to know the formatting string.
```python
nepali_date = NepaliDate.strpdate('06/20/2076', '%m/%d/%Y')
print(nepali_date, type(nepali_date))
```
