Formatting
==========

Date in ISO-format ie. "YYYY-MM-DD"
-----------------------------------

..  code-block:: python

    >>> NepaliDate(2076, 4, 2).isoformat()
    '2076-04-02'


strfdate
--------

Similar API to datetime.datetime.strftime. NepaliDate to formatted string. Follow the formatting table to know the formatting string

..  code-block:: python

    >>> NepaliDate(2075, 10, 10).strfdate('%Y/%m/%d')
    '2075/10/10'

strpdate
--------

Similar API to datetime.datetime.strptime. Return NepaliDate instance if string and format matches. Follow the formatting table to know the formatting string

..  code-block:: python

    >>> NepaliDate.strpdate('06/20/2076', '%m/%d/%Y')
    nepali_date.NepaliDate(2076, 6, 20)


strfdate() and strpdate() Format Codes
--------------------------------------

..  csv-table::
    :file: formatting.csv
    :header-rows: 1


Format specifier for lang="eng"::

    >>> date_BS = NepaliDate(2076, 4, 7)
    >>> print("{0:B} {0:d}".format(date_BS))
    Shrawan 07


Format specifier for lang="nep"::

    >>> date_BS = NepaliDate(2076, 8, 15, lang="nep")
    >>> print("{0:B} {0:d}".format(date_BS))
    मंसिर १५
