import unittest
import datetime

from nepali_date.date import (
        MIN_DATE,
        MAX_DATE,
        REFERENCE_DATE_AD,
        NepaliDate,
)

class NepaliDateTest(unittest.TestCase):
        def test_to_english_date(self):
            date_nepali = NepaliDate(MIN_DATE['year'], MIN_DATE['month'], MIN_DATE['day'])
            date_english = date_nepali.to_english_date()

            self.assertEqual(date_english.year, REFERENCE_DATE_AD['year'])
            self.assertEqual(date_english.month, REFERENCE_DATE_AD['month'])
            self.assertEqual(date_english.day, REFERENCE_DATE_AD['day'])
            # TODO: add more tests


        def test_to_nepali_date(self):
            date_english = datetime.date(REFERENCE_DATE_AD['year'], REFERENCE_DATE_AD['month'], REFERENCE_DATE_AD['day'])
            date_nepali = NepaliDate.to_nepali_date(date_ad=date_english)

            self.assertEqual(date_nepali.year, MIN_DATE['year'])
            self.assertEqual(date_nepali.month, MIN_DATE['month'])
            self.assertEqual(date_nepali.day, MIN_DATE['day'])
            # TODO: add more tests


if __name__ == "__main__":
    unittest.main()

