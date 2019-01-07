# Nepali Date (Bikram Sambat B.S) API 

The API similar to datetime.date() that works on the BS date instead of AD.

### Installation
 
You can install the Nepali Date from PyPI:

    pip install nepali-date


### How to use

>  BS Date today

        from nepali_date import NepaliDate
        
        # print today BS date
        print(NepaliDate.today())


>  Creating NepaliDate instance

        from nepali_date import NepaliDate
        
        my_birthday = NepaliDate(2051, 10, 1)
        # or
        my_birthday = NepaliDate('2051', '10', '1')

> Adding/Subtracting datetime.timedelta to NepaliDate instance
        
        import datetime
        
        from nepali_date import NepaliDate
        
        my_birthday = NepaliDate(2051, 10, 1)
        
        hundred_days_after_my_birthday = my_birthday + timedelta(days=100)
        hundred_days_before_my_birthday = my_birthday - timedelta(days=100)

> Converting datetime.date to NepaliDate or vice-versa
        
        import datetime
        
        from nepali_date import NepaliDate
        
        my_birthday_in_ad = datetime.date(1995, 10, 15)
        my_birthday_in_bs = NepaliDate.to_nepali_date(my_birthday_in_ad)
        
        my_birthday = NepaliDate(2051, 10, 1)
        my_birthday_in_ad = my_birthday.to_english_date()
