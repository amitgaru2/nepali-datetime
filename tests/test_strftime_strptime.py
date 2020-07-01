import nepali_datetime


class TestStrftime:

    def test_strftime_date(self):
        dt = nepali_datetime.date(2077, 6, 4)
        assert dt.strftime("%m/%d/%Y") == "06/04/2077"
        assert dt.strftime("%A of %B %d %y") == "Sunday of Asoj 04 77"
        assert dt.strftime("%a %b") == "Sun Aso"

    def test_strftime_datetime(self):
        dt = nepali_datetime.datetime(2052, 10, 29, 15, 22, 50, 2222)
        assert dt.strftime("%m/%d/%Y %I:%M:%S.%f") == "10/29/2052 03:22:50.002222"


class TestStrptime:

    def test_strptime_date(self):
        assert nepali_datetime.datetime.strptime("2011-10-11", "%Y-%m-%d").date() == nepali_datetime.date(2011, 10, 11)

    def test_strptime_datetime(self):
        assert nepali_datetime.datetime.strptime("Ashar 23 2025 10:00:00",
                                                 "%B %d %Y %H:%M:%S") == nepali_datetime.datetime(2025, 3, 23, 10, 0, 0)
