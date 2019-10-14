import datetime

from nepali_date.date import MIN_DATE, REFERENCE_DATE_AD, NepaliDate

RANDOM_CONVERSION_MAPS = [{'nep': {'year': 2076, 'month': 6, 'day': 27},
                           'eng': {'year': 2019, 'month': 10, 'day': 14}},
                          {'nep': {'year': 2013, 'month': 2, 'day': 8},
                           'eng': {'year': 1956, 'month': 5, 'day': 21}}]


class TestConversion:
    """Test English to Nepali Date Conversion and Nepali to English Date Conversion."""

    def test_to_english_date(self):
        date_nepali = NepaliDate(MIN_DATE['year'], MIN_DATE['month'], MIN_DATE['day'])
        date_english = date_nepali.to_english_date()

        assert date_english.year == REFERENCE_DATE_AD['year']
        assert date_english.month == REFERENCE_DATE_AD['month']
        assert date_english.day == REFERENCE_DATE_AD['day']

    def test_to_nepali_date(self):
        date_english = datetime.date(REFERENCE_DATE_AD['year'], REFERENCE_DATE_AD['month'], REFERENCE_DATE_AD['day'])
        date_nepali = NepaliDate.to_nepali_date(date_ad=date_english)

        assert date_nepali.year == MIN_DATE['year']
        assert date_nepali.month == MIN_DATE['month']
        assert date_nepali.day == MIN_DATE['day']

    def test_random_conversions(self):
        for rd_maps in RANDOM_CONVERSION_MAPS:
            nep_date = NepaliDate(**rd_maps['nep'])
            eng_date = datetime.date(**rd_maps['eng'])
            eng_date_trans = nep_date.to_english_date()

            assert eng_date_trans == eng_date
