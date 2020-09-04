import datetime

import nepali_datetime


class TestDateMethods:
    """Test helper methods of nepali_datetime.date ."""

    def test_today(self):
        dt = nepali_datetime.date.today()
        assert nepali_datetime.MINYEAR <= dt.year <= nepali_datetime.MAXYEAR
        assert 1 <= dt.day <= 32
        assert 1 <= dt.month <= 12


class TestDatetimeMethods:
    """Test helper methods of nepali_datetime.datetime ."""

    def test_now(self):
        dt = nepali_datetime.datetime.now()
        assert nepali_datetime.MINYEAR <= dt.year <= nepali_datetime.MAXYEAR
        assert 1 <= dt.day <= 32
        assert 1 <= dt.month <= 12
        assert 0 <= dt.hour <= 23
        assert 0 <= dt.minute <= 59
        assert 0 <= dt.second <= 59
        assert 0 <= dt.microsecond <= 999999
        assert isinstance(dt.tzinfo, nepali_datetime.UTC0545)

    def test_utcnow(self):
        dt = nepali_datetime.datetime.now()
        utc_dt = dt.utcnow()
        utc_545 = utc_dt + datetime.timedelta(hours=5, minutes=45)
        assert dt.year == utc_545.year
        assert dt.month == utc_545.month
        assert dt.day == utc_545.day
        assert dt.hour == utc_545.hour
        assert dt.minute == utc_545.minute
