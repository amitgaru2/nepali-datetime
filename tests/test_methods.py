import datetime

import nepali_datetime


class TestDateMethods:
    """Test helper methods of nepali_datetime.date ."""

    def test_init(self):
        dt = nepali_datetime.date(2075, 5, 20)
        assert dt.year == 2075
        assert dt.month == 5
        assert dt.day == 20

    def test_today(self):
        ndt = nepali_datetime.date.today()
        assert nepali_datetime.MINYEAR <= ndt.year <= nepali_datetime.MAXYEAR
        assert 1 <= ndt.day <= 32
        assert 1 <= ndt.month <= 12

        dt = nepali_datetime.date.from_datetime_date(
            (datetime.datetime.utcnow() + datetime.timedelta(seconds=nepali_datetime.NEPAL_TIME_UTC_OFFSET)).date()
        )
        assert ndt == dt


class TestDatetimeMethods:
    """Test helper methods of nepali_datetime.datetime ."""

    def test_init(self):
        dt = nepali_datetime.datetime(2033, 2, 10, 10, 5, 30, 123456)
        assert dt.year == 2033
        assert dt.month == 2
        assert dt.day == 10
        assert dt.hour == 10
        assert dt.minute == 5
        assert dt.second == 30
        assert dt.microsecond == 123456

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

    def test_timestamp(self):
        dt = nepali_datetime.datetime(2078, 2, 23)
        ad_dt = datetime.datetime(2021, 6, 6, tzinfo=nepali_datetime.UTC0545())
        assert dt.timestamp() == ad_dt.timestamp()
