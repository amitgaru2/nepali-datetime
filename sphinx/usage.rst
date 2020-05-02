Usage
=====

Importing the class::

    from nepali_date import NepaliDate


Creating instance of NepaliDate::

    >>> date_BS = NepaliDate(2055, 9, 12)
    >>> date_BS
    nepali_date.NepaliDate(2055, 9, 12)

    >>> date_BS = NepaliDate('2053', '11', '11')
    >>> date_BS
    nepali_date.NepaliDate(2053, 11, 11)


Creating instance of NepaliDate with output on Nepali language format::

    >>> date_BS = NepaliDate('2055', '5', '17', lang='nep')
    >>> date_BS
    nepali_date.NepaliDate(२०५५, ५, १७)


Adding/Subtracting datetime.timedelta to NepaliDate instance::

    >>> from datetime import timedelta

    >>> date_BS = NepaliDate(2077, 1, 1)
    >>> forty_days_after = date_BS + timedelta(days=40)
    nepali_date.NepaliDate(2077, 2, 10)

    >>> twenty_days_b4 = date_BS - timedelta(days=40)
    >>> twenty_days_b4
    nepali_date.NepaliDate(2076, 11, 21)


Converting datetime.date to NepaliDate or vice-versa::

    >>> from datetime import date

    >>> date_AD = date(1995, 1, 15)
    >>> NepaliDate.to_nepali_date(date_AD)
    nepali_date.NepaliDate(2051, 10, 1)

    >>> date_BS = NepaliDate(2069, 8, 15)
    >>> date_BS.to_english_date()
    datetime.date(2012, 11, 30)


Nepali Date (B.S) today
-----------------------
.. code-block:: python

    >>> NepaliDate.today()
    nepali_date.NepaliDate(2077, 1, 20)

Monthly Nepali Date (B.S) calendar
----------------------------------
..  code-block:: python

    >>> NepaliDate.calendar()
                  Baisakh 2077
    Sun  Mon  Tue  Wed  Thu  Fri  Sat
           1    2    3    4    5    6
      7    8    9   10   11   12   13
     14   15   16   17   18   19   20
     21   22   23   24   25   26   27
     28   29   30   31

    >>> NepaliDate.calendar(justify=7)
                          Baisakh 2077
    Sun     Mon     Tue     Wed     Thu     Fri     Sat
              1       2       3       4       5       6
      7       8       9      10      11      12      13
     14      15      16      17      18      19      20
     21      22      23      24      25      26      27
     28      29      30      31

    >>> NepaliDate.calendar(lang="nep", justify=7)
                       बैशाख २०७७
    आइत     सोम    मंगल     बुध    बिहि    शक्र     शनि
              १       २       ३       ४       ५       ६
      ७       ८       ९      १०      ११      १२      १३
     १४      १५      १६      १७      १८      १९      २०
     २१      २२      २३      २४      २५      २६      २७
     २८      २९      ३०      ३१

