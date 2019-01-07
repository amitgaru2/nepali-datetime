import os
import csv
import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__))
CALENDAR_PATH = os.path.join(BASE_DIR, 'data', 'calendar_bs.csv')

MIN_DATE = {
    'year': 1975,
    'month': 1,
    'day': 1
}

MAX_DATE = {
    'year': 2100,
    'month': 12,
    'day': 32
}

REFERENCE_DATE_AD = {
    'year': 1918,
    'month': 4,
    'day': 13
}

# TODO: document the code
# TODO: format specifier for different output date results
# TODO: write tests


class NepaliDateMeta(type):

    @staticmethod
    def load_calendar():
        with open(CALENDAR_PATH, 'r') as calendar_file:
            file = csv.reader(calendar_file)
            headers = next(file)
            calendar = {}
            for row in file:
                calendar[int(row[0])] = [int(days) for days in row[1:]]

            return calendar

    def __init__(cls, cls_name, superclasses, attr_dict):
        cls.min = cls(**MIN_DATE, meta=True)
        cls.max = cls(**MAX_DATE, meta=True)
        cls.calendar = cls.load_calendar()
        super().__init__(cls_name, superclasses, attr_dict)


class NepaliDate(metaclass=NepaliDateMeta):

    def __init__(self, year, month, day, **kwargs):
        self.year, self.month, self.day = self.clean_attrs(year=year, month=month, day=day)
        if not ('meta' in kwargs and kwargs['meta']):
            self.post_validation()

    def __str__(self):
        year = str(self.year)
        month = '0{}'.format(self.month) if self.month < 10 else self.month
        day = '0{}'.format(self.day) if self.day < 10 else self.day

        return "BS {}/{}/{}".format(year, month, day)

    def __repr__(self):
        return "nepali_datetime.NepaliDate({}, {}, {})".format(self.year, self.month, self.day)

    @staticmethod
    def clean_attrs(year, month, day):
        year, month, day = str(year), str(month), str(day)

        if not (year.isnumeric() and month.isnumeric() and day.isnumeric()):
            raise ValueError("Invalid year or month or day.")

        return int(year), int(month), int(day)

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, year):
        if len(str(year)) != 4:
            raise ValueError("Invalid year. Expected 4 digits year like -> 2075.")

        self.__year = year

    @property
    def month(self):
        return self.__month

    @month.setter
    def month(self, month):
        if len(str(month)) not in [1, 2]:
            raise ValueError("Invalid month. Expected 1 or 2 digits month like -> 1 or 01.")

        elif int(month) > 12 or int(month) < 1:
            raise ValueError("Invalid month.")

        self.__month = month

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        if len(str(day)) not in [1, 2]:
            raise ValueError("Invalid day. Expected 1 or 2 digits day like -> 1 or 01.")

        elif int(day) > 32 or int(day) < 0:
            raise ValueError("Invalid day.")

        self.__day = day

    def post_validation(self):
        if self.min > self:
            raise ValueError("Date {} is out of range.".format(self))

        if self.max < self:
            raise ValueError("Date {} is out of range.".format(self))

        if self.__day > NepaliDate.calendar[self.__year][self.__month-1]:
            raise ValueError("Invalid nepali date {}.".format(self))

    def __eq__(self, other):
        if not isinstance(other, NepaliDate):
            raise TypeError(
                "'==' not supported between instances of '{.__name__}' and '{.__name__}'".format(type(self), type(other)))

        return self.__year == other.__year and self.__month == other.__month and self.__day == other.__day

    def __lt__(self, other):
        if not isinstance(other, NepaliDate):
            raise TypeError(
                "'<' not supported between instances of '{.__name__}' and '{.__name__}'".format(type(self), type(other)))

        if self.__year == other.__year:
            if self.__month == other.__month:
                if self.__day < other.__day:
                    return True
                return False

            elif self.__month < other.__month:
                return True
            return False

        elif self.__year < other.__year:
            return True
        return False

    def __add__(self, other):
        """ The core logic of the algorithm. """

        if not isinstance(other, datetime.timedelta):
            raise TypeError(
                "Unsupported operand type(s) for +: {.__name__} and {.__name__}.".format(type(self), type(other)))

        delta_years, delta_months = 0, 0
        delta_days = other.days

        total_remaining_days_this_year = NepaliDate.total_days(self.year) - (
                sum(
                    NepaliDate.calendar[self.year][:self.month - 1]
                ) + self.day
        )
        from_year, from_month, from_day = self.year, self.month, self.day

        if delta_days > total_remaining_days_this_year:
            delta_days -= total_remaining_days_this_year
            from_year += 1
            from_month = 1
            from_day = 0

        if from_year > MAX_DATE['year']:
            raise OverflowError("Resulting date out of range.")

        delta_years = 0
        if delta_days > NepaliDate.total_days(from_year):
            for year in range(from_year, MAX_DATE['year'] + 1):
                total_days = NepaliDate.total_days(year)
                if delta_days > total_days:
                    delta_days -= total_days
                    delta_years += 1

                else:
                    break

        from_year += delta_years
        if from_year > MAX_DATE['year']:
            raise OverflowError("Resulting date out of range.")

        if from_year == self.year:
            total_remaining_days_this_month = NepaliDate.calendar[from_year][from_month - 1] - from_day
            if delta_days > total_remaining_days_this_month:
                delta_days -= total_remaining_days_this_month
                from_month += 1
                from_day = 0

        for month_days in NepaliDate.calendar[from_year][from_month - 1:]:
            if delta_days > month_days:
                delta_days -= month_days
                delta_months += 1

            else:
                break

        from_month += delta_months
        from_day += delta_days

        return NepaliDate(year=from_year, month=from_month, day=from_day)

    def __sub__(self, other):
        """ The core logic of the algorithm. """

        if not isinstance(other, datetime.timedelta):
            raise TypeError(
                "Unsupported operand type(s) for +: {.__name__} and {.__name__}.".format(type(self), type(other)))

        delta_years, delta_months = 0, 0
        delta_days = other.days

        total_passed_days_this_year = sum(
            NepaliDate.calendar[self.year][:self.month - 1]
        ) + self.day

        from_year, from_month, from_day = self.year, self.month, self.day

        if delta_days >= total_passed_days_this_year:
            delta_days -= total_passed_days_this_year
            from_year = self.year - 1
            from_month = 12

            if from_year < MIN_DATE['year']:
                raise OverflowError("Resulting date out of range.")

            from_day = NepaliDate.calendar[from_year][11]

        if delta_days >= NepaliDate.total_days(from_year):
            for year in range(from_year, MIN_DATE['year'] - 1, -1):
                total_days = NepaliDate.total_days(year)
                if delta_days > total_days:
                    delta_days -= total_days
                    delta_years += 1

                else:
                    break

        from_year -= delta_years
        if from_year < MIN_DATE['year']:
            raise OverflowError("Resulting date out of range.")

        if from_year == self.year:
            total_passed_days_this_month = from_day
            if delta_days >= total_passed_days_this_month:
                delta_days -= total_passed_days_this_month
                from_month -= 1
                from_day = NepaliDate.calendar[from_year][from_month-1]

        for month_days in NepaliDate.calendar[from_year][from_month-1::-1]:
            if delta_days >= month_days:
                delta_days -= month_days
                from_month -= 1
                from_day = NepaliDate.calendar[from_year][from_month-1]

            else:
                break

        from_day -= delta_days

        return NepaliDate(year=from_year, month=from_month, day=from_day)

    @staticmethod
    def total_days(year):
        assert year in NepaliDate.calendar, "Year {} not in range.".format(year)
        return sum(NepaliDate.calendar[year])

    @staticmethod
    def delta_with_reference_ad(date: datetime.date) -> datetime.timedelta:
        delta = date - datetime.date(**REFERENCE_DATE_AD)
        return delta

    def delta_with_reference_bs(self):
        delta = 0
        for year in range(self.min.__year, self.__year):
            delta += NepaliDate.total_days(year)

        for month in range(1, self.__month):
            delta += NepaliDate.calendar[self.__year][month-1]

        delta += self.__day - 1
        return datetime.timedelta(days=delta)

    @staticmethod
    def today():
        date_today_ad = datetime.datetime.today().date()
        delta = NepaliDate.delta_with_reference_ad(date_today_ad)
        date_today_bs = NepaliDate.min + delta
        return date_today_bs

    @staticmethod
    def to_nepali_date(date_ad: datetime.date):
        if not isinstance(date_ad, datetime.date):
            raise TypeError("Unsupported type {}.".format(type(date_ad)))
        delta = NepaliDate.delta_with_reference_ad(date_ad)
        date_bs = NepaliDate.min + delta
        return date_bs

    def to_english_date(self):
        delta = self.delta_with_reference_bs()
        return datetime.date(**REFERENCE_DATE_AD) + delta
