# Nepali Date (Bikram Sambat B.S) API 

The API similar to datetime.date() that works on the BS date instead of AD.

### Installation
 
You can install the Nepali Date from PyPI: ```pip install nepali-date```


### How to use

>  BS Date today
```python
from nepali_date import NepaliDate
        
# print today BS date
print(NepaliDate.today())
```

>  Creating NepaliDate instance
```python
from nepali_date import NepaliDate
        
my_birthday = NepaliDate(2051, 10, 1)
# or
my_birthday = NepaliDate('2051', '10', '1')
```
> Adding/Subtracting datetime.timedelta to NepaliDate instance
```python 
import datetime
from nepali_date import NepaliDate

my_birthday = NepaliDate(2051, 10, 1)
hundred_days_after_my_birthday = my_birthday + datetime.timedelta(days=100)
hundred_days_before_my_birthday = my_birthday - datetime.timedelta(days=100)
```
> Converting datetime.date to NepaliDate or vice-versa
```python
import datetime

from nepali_date import NepaliDate

my_birthday_in_ad = datetime.date(1995, 10, 15)
my_birthday_in_bs = NepaliDate.to_nepali_date(my_birthday_in_ad)

my_birthday = NepaliDate(2051, 10, 1)
my_birthday_in_ad = my_birthday.to_english_date()
```
### Monthly Calendar
> Current nepali month calendar
```python
from nepali_date import NepaliDate
NepaliDate.calendar()
```
![Screenshot](screenshots/nepali_monthly_calendar.PNG)


### Date in isoformat() 'YYYY-MM-DD'
```python
dt = NepaliDate(2076, 4, 2)
print(dt.isoformat())
# outputs 2076-04-02
```

### Date display format
Format Specifier | Meaning | Example
--- | --- | ---
```{:d}``` | Day of the month as a zero-padded decimal number. | 01, 02, ..., 32
```{:b}``` | Month as abbreviated name. | Bai, Jes, ..., Cha
```{:B}``` | Month as full name. | Baishak, Jestha, ..., Chait
```{:m}``` | Month as a zero-padded decimal number. | 01, 02, ..., 12
```{:y}``` | Year without century as a zero-padded decimal number. | 00, 01, ..., 99
```{:Y}``` | Year with century as a decimal number. | 0001, 0002, ..., 2075, 2076, ..., 9999

```python
dt = NepaliDate(2076, 4, 7)
print("{0:B} {0:d}".format(dt))
# outputs Shrawan 07
```