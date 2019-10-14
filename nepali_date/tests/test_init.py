from nepali_date.date import (MIN_DATE,
                              MAX_DATE,
                              NepaliDate)


class TestInit:
    """Test attributes initialized when a instance of the class is created."""

    def test_min_date(self):
        nep_date = NepaliDate(2051, 10, 1)
        assert MIN_DATE['year'] == nep_date.min.year
        assert MIN_DATE['month'] == nep_date.min.month
        assert MIN_DATE['day'] == nep_date.min.day

    def test_max_date(self):
        nep_date = NepaliDate(2051, 10, 1)
        assert MAX_DATE['year'] == nep_date.max.year
        assert MAX_DATE['month'] == nep_date.max.month
        assert MAX_DATE['day'] == nep_date.max.day
