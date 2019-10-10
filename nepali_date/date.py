import re
import os
import csv
import datetime
import platform

from functools import reduce

BASE_DIR = os.path.join(os.path.dirname(__file__))
CALENDAR_PATH = os.path.join(BASE_DIR, 'data', 'calendar_bs.csv')
MIN_DATE = {'year': 1975, 'month': 1, 'day': 1}
MAX_DATE = {'year': 2100, 'month': 12, 'day': 30}
REFERENCE_DATE_AD = {'year': 1918, 'month': 4, 'day': 13}
WEEKDAYS_MAPPER = {6: ('Sun', 'Su'), 0: ('Mon', 'Mo'), 1: ('Tue', 'Tu'), 2: ('Wed', 'We'), 3: ('Thu', 'Th'),
                   4: ('Fri', 'Fr'), 5: ('Sat', 'Sa')}
NEPALI_MONTHS = (("Baisakh", "Bai"), ("Jestha", "Jes"), ("Ashar", "Ash"), ("Shrawan", "Shr"), ("Bhadra", "Bha"),
                 ("Asoj", "Aso"), ("Kartik", "Kar"), ("Mangsir", "Man"), ("Poush", "Pou"), ("Magh", "Mag"),
                 ("Falgun", "Fal"), ("Chait", "Cha"))
TRANSLATION_MAP = {
    'month': {'Baisakh': 'बैशाख', 'Jestha': 'जेष्ठ', 'Ashar': 'आषाढ', 'Shrawan': 'श्रावन', 'Bhadra': 'भाद्र',
              'Asoj': 'असोज', 'Kartik': 'कार्तिक', 'Mangsir': 'मंसिर', 'Poush': 'पौष', 'Magh': 'माघ', 'Falgun': 'फागुन',
              'Chait': 'चैत्र', 'Bai': 'बैशाख', 'Jes': 'जेष्ठ', 'Ash': 'आषाढ', 'Shr': 'श्रावन', 'Bha': 'भाद्र',
              'Aso': 'असोज', 'Kar': 'कार्तिक', 'Man': 'मंसिर', 'Pou': 'पौष', 'Mag': 'माघ', 'Fal': 'फागुन',
              'Cha': 'चैत्र'},
        'day': {'Sun': 'आइत', 'Mon': 'सोम', 'Tue': 'मंगल', 'Wed': 'बुध', 'Thu': 'बिहि', 'Fri': 'शक्र', 'Sat': 'शनि'},
    'digits': {'0': '०', '1': '१', '2': '२', '3': '३', '4': '४', '5': '५', '6': '६', '7': '७', '8': '८', '9': '९'}
}

FORMAT_MAP = {'Y': lambda x: x.translated_year,
              'y': lambda x: NepaliDate.translate(x.lang, str(x.year)[2:]),
              'm': lambda x: NepaliDate.translate(x.lang, '0{}'.format(x.month) if x.month < 10 else str(x.month)),
              'b': lambda x: NepaliDate.translate(x.lang, NEPALI_MONTHS[x.month - 1][1], to_translate='month'),
              'B': lambda x: NepaliDate.translate(x.lang, NEPALI_MONTHS[x.month - 1][0], to_translate='month'),
              'd': lambda x: NepaliDate.translate(x.lang, '0{}'.format(x.day) if x.day < 10 else str(x.day))}


class NepaliDateMeta(type):

    @staticmethod
    def load_calendar():
        calendar = dict()
        with open(CALENDAR_PATH, 'r') as calendar_file:
            file = csv.reader(calendar_file)
            headers = next(file)
            for row in file:
                calendar[int(row[0])] = [int(days) for days in row[1:]]

        return calendar

    def __init__(cls, what, bases=None, dict=None):
        cls.calendar_data = cls.load_calendar()
        cls.min = cls(**MIN_DATE)
        cls.max = cls(**MAX_DATE)
        super().__init__(what, bases, dict)


class NepaliDate(metaclass=NepaliDateMeta):

    def __init__(self, year, month, day, lang='eng'):
        self.lang = lang
        self.year, self.month, self.day = self.clean_attrs(year=year, month=month, day=day)
        if self.day > self.calendar_data[self.year][self.month - 1]:
            raise ValueError("Trying to create invalid Nepali Date.")

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
        if not MIN_DATE['year'] <= year <= MAX_DATE['year']:
            raise ValueError("Year {} is out of range.".format(year))
        self.__year = year

    @property
    def translated_year(self):
        return NepaliDate.translate(self.lang, str(self.__year)) if self.lang == 'nep' else str(self.__year)

    @property
    def month(self):
        return self.__month

    @month.setter
    def month(self, month):
        if not 1 <= month <= 12:
            raise ValueError("Invalid month.")
        self.__month = month

    @property
    def translated_month(self):
        return NepaliDate.translate(self.lang, str(self.__month)) if self.lang == 'nep' else str(self.__month)

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, day):
        if not 1 <= day <= 32:
            raise ValueError("Invalid day.")
        self.__day = day

    @property
    def translated_day(self):
        return NepaliDate.translate(self.lang, str(self.__day)) if self.lang == 'nep' else str(self.__day)

    @property
    def lang(self):
        return self.__lang

    @lang.setter
    def lang(self, lang):
        assert lang in ('eng', 'nep'), 'Language must be either "eng" or "nep".'
        self.__lang = lang

    @staticmethod
    def translate(lang, string, to_translate='digits'):
        assert to_translate in TRANSLATION_MAP.keys()

        if lang == 'nep':
            if to_translate in ('month', 'day'):
                return TRANSLATION_MAP[to_translate][string]
            return ''.join([TRANSLATION_MAP['digits'][i] for i in string])
        return string

    def __str__(self):
        month = '0{}'.format(self.month) if self.month < 10 else str(self.month)
        day = '0{}'.format(self.day) if self.day < 10 else str(self.day)

        return "{} {}/{}/{}".format('बि. सं.' if self.lang == 'nep' else 'BS',
                                    NepaliDate.translate(self.lang, str(self.year)),
                                    NepaliDate.translate(self.lang, month),
                                    NepaliDate.translate(self.lang, day))

    def __repr__(self):
        return "nepali_date.NepaliDate({}, {}, {})".format(self.translated_year, self.translated_month,
                                                           self.translated_day)

    def __format__(self, format_spec):
        formatter = FORMAT_MAP.get(format_spec, None)
        return formatter(self) if formatter is not None else ''

    def isoformat(self):
        month = '0{}'.format(self.month) if self.month < 10 else str(self.month)
        day = '0{}'.format(self.day) if self.day < 10 else str(self.day)

        return "{}-{}-{}".format(NepaliDate.translate(self.lang, str(self.year)),
                                 NepaliDate.translate(self.lang, month),
                                 NepaliDate.translate(self.lang, day))

    def __eq__(self, other):
        if not isinstance(other, NepaliDate):
            raise TypeError(
                "'==' not supported between instances of '{.__name__}' and '{.__name__}'".format(type(self),
                                                                                                 type(other)))

        return self.__year == other.__year and self.__month == other.__month and self.__day == other.__day

    def __lt__(self, other):
        if not isinstance(other, NepaliDate):
            raise TypeError(
                "'<' not supported between instances of '{.__name__}' and '{.__name__}'".format(type(self),
                                                                                                type(other)))

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
                    NepaliDate.calendar_data[self.year][:self.month - 1]
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
            total_remaining_days_this_month = NepaliDate.calendar_data[from_year][from_month - 1] - from_day
            if delta_days > total_remaining_days_this_month:
                delta_days -= total_remaining_days_this_month
                from_month += 1
                from_day = 0

        for month_days in NepaliDate.calendar_data[from_year][from_month - 1:]:
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
            NepaliDate.calendar_data[self.year][:self.month - 1]
        ) + self.day

        from_year, from_month, from_day = self.year, self.month, self.day

        if delta_days >= total_passed_days_this_year:
            delta_days -= total_passed_days_this_year
            from_year = self.year - 1
            from_month = 12

            if from_year < MIN_DATE['year']:
                raise OverflowError("Resulting date out of range.")

            from_day = NepaliDate.calendar_data[from_year][11]

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
                from_day = NepaliDate.calendar_data[from_year][from_month - 1]

        for month_days in NepaliDate.calendar_data[from_year][from_month - 1::-1]:
            if delta_days >= month_days:
                delta_days -= month_days
                from_month -= 1
                from_day = NepaliDate.calendar_data[from_year][from_month - 1]

            else:
                break

        from_day -= delta_days

        return NepaliDate(year=from_year, month=from_month, day=from_day)

    @staticmethod
    def total_days(year):
        assert year in NepaliDate.calendar_data, "Year {} not in range.".format(year)
        return sum(NepaliDate.calendar_data[year])

    @staticmethod
    def delta_with_reference_ad(date: datetime.date) -> datetime.timedelta:
        delta = date - datetime.date(**REFERENCE_DATE_AD)
        return delta

    def delta_with_reference_bs(self):
        delta = 0
        for year in range(self.min.__year, self.__year):
            delta += NepaliDate.total_days(year)

        for month in range(1, self.__month):
            delta += NepaliDate.calendar_data[self.__year][month - 1]

        delta += self.__day - 1
        return datetime.timedelta(days=delta)

    @staticmethod
    def today(lang='eng'):
        date_today_ad = datetime.datetime.today().date()
        delta = NepaliDate.delta_with_reference_ad(date_today_ad)
        date_today_bs = NepaliDate.min + delta
        date_today_bs.lang = lang
        return date_today_bs

    @staticmethod
    def weekday():
        return WEEKDAYS_MAPPER[datetime.datetime.today().weekday()][0]

    @staticmethod
    def calendar(lang='eng', justify=4):
        today = NepaliDate.today()
        weekdays = ' '.join(
            [NepaliDate.translate(lang, i[0], to_translate='day').rjust(justify) for i in WEEKDAYS_MAPPER.values()])
        month_year = '{} {}'.format(NepaliDate.translate(lang, NEPALI_MONTHS[today.month - 1][0], to_translate='month'),
                                    NepaliDate.translate(lang, str(today.year))).center(len(weekdays))
        start_day = (NepaliDate(year=today.year, month=today.month, day=1).to_english_date().weekday() + 1) % 7
        total_days_this_month = NepaliDate.calendar_data[today.year][today.month - 1]
        days = [' ' * justify for i in range(start_day)]
        for i in range(1, total_days_this_month + 1):
            days.append(NepaliDate.translate(lang, str(i)).rjust(justify))
        days[days.index(NepaliDate.translate(lang, str(today.day)).rjust(justify))] = '\033[0;31m {}\033[0m'.format(
            NepaliDate.translate(lang, str(today.day))).rjust(11 + justify)
        week_days, temp = list(), list()
        for i, v in enumerate(days, 1):
            temp.append(v)
            if i % 7 == 0:
                week_days.append(temp)
                temp = list()
        if len(temp) > 0:
            week_days.append(temp)
        days_disp = '\n'.join([' '.join(i) for i in week_days])
        if platform.system() == 'Windows':
            os.system("COLOR 07")
        print("{}\n{}\n{}".format(month_year, weekdays, days_disp))

    @staticmethod
    def to_nepali_date(date_ad: datetime.date, lang='eng'):
        if not isinstance(date_ad, datetime.date):
            raise TypeError("Unsupported type {}.".format(type(date_ad)))
        delta = NepaliDate.delta_with_reference_ad(date_ad)
        date_bs = NepaliDate.min + delta
        date_bs.lang = lang
        return date_bs

    def to_english_date(self):
        delta = self.delta_with_reference_bs()
        return datetime.date(**REFERENCE_DATE_AD) + delta

    def strfdate(self, fmt: str) -> str:
        """API similar to datetime.datetime.strftime.
        fmt: the resulting string format with accordance to format specifier.
        Nepali Date object to formatted string."""

        pattern = r'%({})'.format(reduce(lambda x, y: '{}|{}'.format(x, y), FORMAT_MAP.keys()))
        for f in re.findall(pattern, fmt):
            fmt = fmt.replace('%{}'.format(f), FORMAT_MAP[f](self))
        return fmt

    @classmethod
    def strpdate(cls, string: str, fmt="%Y/%m/%d", lang='eng'):
        """API similar to datetime.datetime.strptime.
        string: NepaliDate in string format.
        fmt: format matching the string with accordance to format specifier.
        Returns NepaliDate instance if the string and format matches."""

        pattern = r'%({})'.format(reduce(lambda x, y: '{}|{}'.format(x, y), FORMAT_MAP.keys()))
        params = re.findall(pattern, fmt)
        if len(params) != len(set(params)):
            raise ValueError("Duplicate format specifier not allowed.")

        for f in params:
            if f == 'Y':
                fmt = fmt.replace('%{}'.format(f), r'(?P<year>\d{4})')
            elif f == 'y':
                fmt = fmt.replace('%{}'.format(f), r'(?P<year>\d{2})')
            elif f == 'm':
                fmt = fmt.replace('%{}'.format(f), r'(?P<month>\d{1,2})')
            elif f == 'd':
                fmt = fmt.replace('%{}'.format(f), r'(?P<day>\d{1,2})')

        fmt = '^{}$'.format(fmt)
        if re.match(fmt, string) is None:
            raise ValueError('Mismatch in "string" and "fmt".')

        _ = {**MIN_DATE, 'lang': lang}
        _.update(re.match(fmt, string).groupdict())
        return cls(**_)
