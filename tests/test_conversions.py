import datetime

import nepali_datetime

from nepali_datetime.config import MINDATE, REFERENCE_DATE_AD

RANDOM_CONVERSION_MAPS = [
    {'bs': {'year': 2013, 'month': 2, 'day': 8}, 'ad': {'year': 1956, 'month': 5, 'day': 21}},
    {'bs': {'year': 2051, 'month': 10, 'day': 1}, 'ad': {'year': 1995, 'month': 1, 'day': 15}},
    {'bs': {'year': 2076, 'month': 6, 'day': 27}, 'ad': {'year': 2019, 'month': 10, 'day': 14}},
    {'bs': {'year': 2077, 'month': 4, 'day': 4}, 'ad': {'year': 2020, 'month': 7, 'day': 19}},
    {'bs': {'year': 2081, 'month': 3, 'day': 31}, 'ad': {'year': 2024, 'month': 7, 'day': 15}}
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
            np_dt = nepali_datetime.date.from_datetime_date(datetime.date(**rd_maps['ad']))
            assert np_dt == nepali_datetime.date(**rd_maps['bs'])

            dt = nepali_datetime.date.to_datetime_date(nepali_datetime.date(**rd_maps['bs']))
            assert dt == datetime.date(**rd_maps['ad'])
