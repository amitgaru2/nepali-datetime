import datetime

import nepali_datetime

from nepali_datetime.config import MINDATE, REFERENCE_DATE_AD

RANDOM_CONVERSION_MAPS = [
    {'nep': {'year': 2076, 'month': 6, 'day': 27}, 'eng': {'year': 2019, 'month': 10, 'day': 14}},
    {'nep': {'year': 2013, 'month': 2, 'day': 8}, 'eng': {'year': 1956, 'month': 5, 'day': 21}},
    {'nep': {'year': 2077, 'month': 4, 'day': 4}, 'eng': {'year': 2020, 'month': 7, 'day': 19}}
]


class TestConversion:
    """Test English to Nepali Date Conversion and Nepali to English Date Conversion."""

    def test_reference_dates(self):
        date_english = datetime.date(
            REFERENCE_DATE_AD['year'], REFERENCE_DATE_AD['month'], REFERENCE_DATE_AD['day']
        )
        date_nepali = nepali_datetime.date.from_datetime_date(from_date=date_english)

        assert date_nepali.year == MINDATE['year']
        assert date_nepali.month == MINDATE['month']
        assert date_nepali.day == MINDATE['day']

    def test_random_conversions(self):
        for rd_maps in RANDOM_CONVERSION_MAPS:
            bs_date = nepali_datetime.date.from_datetime_date(datetime.date(**rd_maps['eng']))
            assert bs_date == nepali_datetime.date(**rd_maps['nep'])
