"""An inspired library from Python's `datetime` library which will operate on top of
Bikram Sambat (B.S) date. Currently supported B.S date range is 1975 - 2100. Most of the code &
documentation are derived from Python3.5 's datetime.py module & later modified to support
nepali_datetime.

Supports >= Python3.5
"""
__version__ = "1.0.8.4"


__author__ = "Amit Garu <amitgaru2@gmail.com>"

import sys
import csv
import time as _time
import math as _math
import datetime as _actual_datetime

from .config import CALENDAR_PATH, MINDATE, MAXDATE, REFERENCE_DATE_AD

MINYEAR = MINDATE['year']
MAXYEAR = MAXDATE['year']

NEPAL_TIME_UTC_OFFSET = 20700

_MONTHNAMES = (None, "Bai", "Jes", "Asa", "Shr", "Bha", "Asw", "Kar", "Man", "Pou", "Mag", "Fal", "Cha")
_FULLMONTHNAMES = (None, "Baishakh", "Jestha", "Asar", "Shrawan", "Bhadau", "Aswin", "Kartik", "Mangsir", "Poush",
                   "Magh", "Falgun", "Chaitra")
_MONTHNAMES_NP = (None, "वैशाख", "जेष्ठ", "असार", "श्रावण", "भदौ", "आश्विन", "कार्तिक", "मंसिर", "पौष",
                  "माघ", "फाल्गुण", "चैत्र")
_DAYNAMES = (None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
_FULLDAYNAMES = (None, "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_FULLDAYNAMES_NP = (None, "सोमबार", "मंगलबार", "बुधवार", "बिहिबार", "शुक्रबार", "शनिबार", "आइतबार")
_DIGIT_NP = "०१२३४५६७८९"
_EPOCH = _actual_datetime.datetime(1970, 1, 1, tzinfo=_actual_datetime.timezone.utc)

_STRFTIME_CUSTOM_MAP = {
    'a': lambda o: '%s' % _DAYNAMES[(o.weekday() % 7) or 7],
    'A': lambda o: '%s' % _FULLDAYNAMES[(o.weekday() % 7) or 7],
    'G': lambda o: '%s' % _FULLDAYNAMES_NP[(o.weekday() % 7) or 7],
    'w': lambda o: '%d' % o.weekday(),
    'd': lambda o: '%02d' % o.day,
    'D': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % o.day),
    'b': lambda o: '%s' % _MONTHNAMES[o.month],
    'B': lambda o: '%s' % _FULLMONTHNAMES[o.month],
    'N': lambda o: '%s' % _MONTHNAMES_NP[o.month],
    'm': lambda o: '%02d' % o.month,
    'n': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % o.month),
    'y': lambda o: '%02d' % (o.year % 100),
    'Y': lambda o: '%d' % o.year,
    'k': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % (o.year % 100)),
    'K': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%d' % o.year),
    'H': lambda o: '%02d' % getattr(o, 'hour', 0),
    'h': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % getattr(o, 'hour', 0)),
    'I': lambda o: '%02d' % (getattr(o, 'hour', 0) % 12,),
    'i': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % (getattr(o, 'hour', 0) % 12,)),
    'p': lambda o: 'AM' if getattr(o, 'hour', 0) < 12 else 'PM',
    'M': lambda o: '%02d' % getattr(o, 'minute', 0),
    'l': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % getattr(o, 'minute', 0)),
    'S': lambda o: '%02d' % getattr(o, 'second', 0),
    's': lambda o: ''.join(_DIGIT_NP[int(i)] for i in '%02d' % getattr(o, 'second', 0)),
    'U': lambda o: '%02d' % ((o.timetuple().tm_yday + 7 - o.weekday()) // 7,),
}

_CALENDAR = {}
_DAYS_BEFORE_YEAR = []

with open(CALENDAR_PATH, 'r') as calendar_file:
    file = csv.reader(calendar_file)
    next(file)
    for row in file:
        _CALENDAR[int(row[0])] = [-1, *[sum(int(j) for j in row[1:i]) for i in range(2, 14)]]
        _DAYS_BEFORE_YEAR.append(sum(int(i) for i in row[1:]) + (_DAYS_BEFORE_YEAR[-1] if _DAYS_BEFORE_YEAR else 0))

_MAXORDINAL = _DAYS_BEFORE_YEAR[-1]


def _build_struct_time(y, m, d, hh, mm, ss, dstflag):
    wday = (_ymd2ord(y, m, d) + 5) % 7
    dnum = _days_before_month(y, m) + d
    return _time.struct_time((y, m, d, hh, mm, ss, wday, dnum, dstflag))


def _format_time(hh, mm, ss, us):
    # Skip trailing microseconds when us==0.
    result = "%02d:%02d:%02d" % (hh, mm, ss)
    if us:
        result += ".%06d" % us
    return result


def _wrap_strftime(object, format):
    # Don't call utcoffset() or tzname() unless actually needed.
    freplace = None  # the string to use for %f
    zreplace = None  # the string to use for %z
    Zreplace = None  # the string to use for %Z

    # Scan format for %z and %Z escapes, replacing as needed.
    newformat = []
    push = newformat.append
    i, n = 0, len(format)
    while i < n:
        ch = format[i]
        i += 1
        if ch == '%':
            if i < n:
                ch = format[i]
                i += 1
                if ch == 'f':
                    if freplace is None:
                        freplace = '%06d' % getattr(object, 'microsecond', 0)
                    newformat.append(freplace)
                elif ch == 'z':
                    if zreplace is None:
                        zreplace = ""
                        if hasattr(object, "utcoffset"):
                            offset = object.utcoffset()
                            if offset is not None:
                                sign = '+'
                                if offset.days < 0:
                                    offset = -offset
                                    sign = '-'
                                h, m = divmod(offset, _actual_datetime.timedelta(hours=1))
                                assert not m % _actual_datetime.timedelta(minutes=1), "whole minute"
                                m //= _actual_datetime.timedelta(minutes=1)
                                zreplace = '%c%02d%02d' % (sign, h, m)
                    assert '%' not in zreplace
                    newformat.append(zreplace)
                elif ch == 'Z':
                    if Zreplace is None:
                        Zreplace = ""
                        if hasattr(object, "tzname"):
                            s = object.tzname()
                            if s is not None:
                                # strftime is going to have at this: escape %
                                Zreplace = s.replace('%', '%%')
                    newformat.append(Zreplace)
                elif ch in _STRFTIME_CUSTOM_MAP.keys():
                    newformat.append(_STRFTIME_CUSTOM_MAP[ch](object))
                else:
                    push('%')
                    push(ch)
            else:
                push('%')
        else:
            push(ch)
    newformat = "".join(newformat)
    return newformat


def _bin_search(key, *arr):
    index = 0
    while True:
        if len(arr) == 1:
            break
        mid = len(arr) // 2 - 1 + len(arr) % 2
        index += mid
        if key == arr[mid]:
            break
        elif key < arr[mid]:
            index -= mid
            arr = arr[:mid + 1]
        else:
            index += 1
            arr = arr[mid + 1:]
    return index


def _check_tzname(name):
    if name is not None and not isinstance(name, str):
        raise TypeError("tzinfo.tzname() must return None or string, not '%s'" % type(name))


def _check_utc_offset(name, offset):
    assert name in ("utcoffset", "dst")
    if offset is None:
        return
    if not isinstance(offset, _actual_datetime.timedelta):
        raise TypeError("tzinfo.%s() must return None "
                        "or _actual_datetime.timedelta, not '%s'" % (name, type(offset)))
    if offset % _actual_datetime.timedelta(minutes=1) or offset.microseconds:
        raise ValueError("tzinfo.%s() must return a whole number "
                         "of minutes, got %s" % (name, offset))
    if not -_actual_datetime.timedelta(1) < offset < _actual_datetime.timedelta(1):
        raise ValueError("%s()=%s, must be must be strictly between "
                         "-timedelta(hours=24) and timedelta(hours=24)" %
                         (name, offset))


def _check_int_field(value):
    if isinstance(value, int):
        return value
    if not isinstance(value, float):
        try:
            value = value.__int__()
        except AttributeError:
            pass
        else:
            if isinstance(value, int):
                return value
            raise TypeError('__int__ returned non-int (type %s)' % type(value).__name__)
        raise TypeError('an integer is required (got type %s)' % type(value).__name__)
    raise TypeError('integer argument expected, got float')


def _days_in_month(year, month):
    assert 1 <= month <= 12, month
    if month == 1:
        return _CALENDAR[year][1]
    return _CALENDAR[year][month] - _CALENDAR[year][month - 1]


def _days_before_year(year):
    """year -> number of days before Baishak 1st of year."""
    assert MINYEAR <= year <= MAXYEAR, "year must be in %s..%s" % (MINYEAR, MAXYEAR)
    if year == MINYEAR:
        return 0
    return _DAYS_BEFORE_YEAR[year - MINYEAR - 1]


def _days_before_month(year, month):
    """year, month -> number of days in year preceding first day of month."""
    assert 1 <= month <= 12, 'month must be in 1..12'
    if month == 1:
        return 0
    return _CALENDAR[year][month - 1]


def _ymd2ord(year, month, day):
    """year, month, day -> ordinal, considering 1975-Bai-01 as day 1."""
    assert 1 <= month <= 12, 'month must be in 1..12'
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, ('day must be in 1..%d' % dim)
    return _days_before_year(year) + _days_before_month(year, month) + day


def _ord2ymd(n):
    year = MINYEAR + _bin_search(n, *_DAYS_BEFORE_YEAR)
    if year > MINYEAR:
        n -= _DAYS_BEFORE_YEAR[year - MINYEAR - 1]
    month = 1 + _bin_search(n, *_CALENDAR[year][1:])
    if month > 1:
        n -= _CALENDAR[year][month - 1]
    return year, month, n


def _check_date_fields(year, month, day):
    year = _check_int_field(year)
    month = _check_int_field(month)
    day = _check_int_field(day)
    if not MINYEAR <= year <= MAXYEAR:
        raise ValueError('year must be in %d..%d' % (MINYEAR, MAXYEAR), year)
    if not 1 <= month <= 12:
        raise ValueError('month must be in 1..12', month)
    dim = _days_in_month(year, month)
    if not 1 <= day <= dim:
        raise ValueError('day must be in 1..%d' % dim, day)
    return year, month, day


def _check_time_fields(hour, minute, second, microsecond):
    hour = _check_int_field(hour)
    minute = _check_int_field(minute)
    second = _check_int_field(second)
    microsecond = _check_int_field(microsecond)
    if not 0 <= hour <= 23:
        raise ValueError('hour must be in 0..23', hour)
    if not 0 <= minute <= 59:
        raise ValueError('minute must be in 0..59', minute)
    if not 0 <= second <= 59:
        raise ValueError('second must be in 0..59', second)
    if not 0 <= microsecond <= 999999:
        raise ValueError('microsecond must be in 0..999999', microsecond)
    return hour, minute, second, microsecond


def _check_tzinfo_arg(tz):
    if tz is not None and not isinstance(tz, UTC0545):
        raise TypeError("tzinfo argument must be None or of a UTC0545 subclass")


def _cmperror(x, y):
    raise TypeError("can't compare '%s' to '%s'" % (type(x).__name__, type(y).__name__))


def _cmp(x, y):
    return 0 if x == y else 1 if x > y else -1


class UTC0545(_actual_datetime.tzinfo):
    _offset = _actual_datetime.timedelta(seconds=NEPAL_TIME_UTC_OFFSET)
    _dst = _actual_datetime.timedelta(0)
    _name = "+0545"

    def utcoffset(self, dt):
        return self.__class__._offset

    def dst(self, dt):
        return self.__class__._dst

    def tzname(self, dt):
        return self.__class__._name

    def fromutc(self, dt):
        """datetime in UTC -> datetime in local time."""

        if not isinstance(dt, datetime) and not isinstance(dt, _actual_datetime.datetime):
            raise TypeError("fromutc() requires a nepali_datetime.datetime or datetime.datetime argument")
        if dt.tzinfo is not self:
            raise ValueError("dt.tzinfo is not self")

        dtoff = dt.utcoffset()
        if dtoff is None:
            raise ValueError("fromutc() requires a non-None utcoffset() "
                             "result")

        dtdst = dt.dst()
        if dtdst is None:
            raise ValueError("fromutc() requires a non-None dst() result")
        delta = dtoff - dtdst
        if delta:
            dt += delta
            dtdst = dt.dst()
            if dtdst is None:
                raise ValueError("fromutc(): dt.dst gave inconsistent "
                                 "results; cannot convert")
        return dt + dtdst


class date:
    __slots__ = ('_year', '_month', '_day')

    def __new__(cls, year, month=None, day=None):
        year, month, day = _check_date_fields(year, month, day)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        return self

    @classmethod
    def fromtimestamp(cls, t):
        """Construct a date from a POSIX timestamp (like time.time())."""
        y, m, d, hh, mm, ss, weekday, jday, dst = _time.gmtime(t + NEPAL_TIME_UTC_OFFSET)
        return cls.from_datetime_date(_actual_datetime.date(y, m, d))

    @classmethod
    def today(cls):
        """Construct a date from time.time()."""
        t = _time.time()
        return cls.fromtimestamp(t)

    @classmethod
    def fromordinal(cls, n):
        """Construct a date from a (MINYEAR, 1, 1).

        Baishak 1 of year 1975 is day 1.  Only the year, month and day are
        non-zero in the result.
        """
        y, m, d = _ord2ymd(n)
        return cls(y, m, d)

    @classmethod
    def from_datetime_date(cls, from_date):
        """Convert datetime.date to nepali_datetime.date (A.D date to B.S).

        Parameters
        ----------
        from_date: datetime.date
            The AD date object to be converted.

        Returns
        -------
        nepali_datetime.date
            The converted nepali_datetime.date object.
        """
        if not isinstance(from_date, _actual_datetime.date):
            raise TypeError("Unsupported type {}.".format(type(from_date)))
        return cls(MINYEAR, 1, 1) + (from_date - _actual_datetime.date(**REFERENCE_DATE_AD))

    def to_datetime_date(self):
        """Convert nepali_datetime.date to datetime.date (B.S date to A.D).

        Returns
        -------
        datetime.date
            The converted datetime.date object.
        """
        return _actual_datetime.date(**REFERENCE_DATE_AD) + _actual_datetime.timedelta(days=self.toordinal() - 1)

    def calendar(self, justify=4):
        format_str = '{:>%s}' % justify

        def _mark_today(indx):
            indx_day = cal[indx].index(format_str.format(self.day))
            cal[indx][indx_day] = '\033[31m{}\033[39m'.format(cal[indx][indx_day])

        total_days_month = _days_in_month(self.year, self.month)
        start_weekday = self.__class__(self.year, self.month, 1).weekday()
        cal = [[('{:^%s}' % ((justify + 1) * 7)).format(self.strftime('%B %Y'))],
               [format_str.format('Sun'), *(format_str.format(j) for j in _DAYNAMES[1:-1])],
               [format_str.format(' ') for _ in range(start_weekday)]]
        cal[-1].extend([format_str.format(j) for j in range(1, 8 - start_weekday)])
        cal_cursor = 8 - start_weekday
        cal_range = [(1, 7 - start_weekday)]

        total_mid_weeks = (total_days_month - cal_cursor) // 7
        for i in range(total_mid_weeks):
            cal_range.append((cal_cursor, cal_cursor + 6))
            cal.append([format_str.format(j) for j in range(cal_cursor, cal_cursor + 7)])
            cal_cursor += 7

        if cal_cursor <= total_days_month:
            cal.append([format_str.format(j) for j in range(cal_cursor, total_days_month + 1)])
            cal_range.append((cal_cursor, total_days_month))

        if sys.platform.startswith('linux'):
            # currently only linux supported
            for i, cr in enumerate(cal_range):
                if cr[0] <= self.day <= cr[1]:
                    _mark_today(-len(cal_range) + i)
                    break

        cal = '\n' + '\n'.join(' '.join(j) for j in cal) + '\n\n'
        sys.stdout.write(cal)

    def __repr__(self):
        return "%s.%s(%d, %d, %d)" % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            self._year,
            self._month,
            self._day
        )

    def ctime(self):
        """Return ctime() style string."""
        weekday = (self.toordinal() + 5) % 7 or 7
        return "%s %s %2d 00:00:00 %04d" % (_DAYNAMES[weekday], _MONTHNAMES[self._month], self._day, self._year)

    def strftime(self, fmt):
        """Format using strftime()."""
        return _wrap_strftime(self, fmt)

    def __format__(self, fmt):
        if not isinstance(fmt, str):
            raise TypeError("must be str, not %s" % type(fmt).__name__)
        if len(fmt) != 0:
            return self.strftime(fmt)
        return str(self)

    def isoformat(self):
        return "%04d-%02d-%02d" % (self._year, self._month, self._day)

    __str__ = isoformat

    @property
    def year(self):
        """year (1975-2100)"""
        return self._year

    @property
    def month(self):
        """month (1-12)"""
        return self._month

    @property
    def day(self):
        """day (1-32)"""
        return self._day

    def timetuple(self):
        """Return local time tuple compatible with time.localtime()."""
        return _build_struct_time(self._year, self._month, self._day, 0, 0, 0, -1)

    def toordinal(self):
        """Baishak 1 of year 1975 is day 1.  Only the year, month and day values contribute to the result."""
        return _ymd2ord(self._year, self._month, self._day)

    def replace(self, year=None, month=None, day=None):
        """Return a new date with new values for the specified fields."""
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        return date(year, month, day)

    def __eq__(self, other):
        if isinstance(other, date):
            return self._cmp(other) == 0
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, date):
            return self._cmp(other) <= 0
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) < 0
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, date):
            return self._cmp(other) >= 0
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, date):
            return self._cmp(other) > 0
        return NotImplemented

    def _cmp(self, other):
        assert isinstance(other, date)
        y, m, d = self._year, self._month, self._day
        y2, m2, d2 = other._year, other._month, other._day
        return _cmp((y, m, d), (y2, m2, d2))

    def __hash__(self):
        return NotImplemented

    def __add__(self, other):
        """Add two nepali_datetime.date objects.
        Parameters
        ----------
        other: datetime.timedelta
            The other object added to self.

        Returns
        -------
        nepali_datetime.date
            The new nepali_datetime.date object after addition operation.
        """
        if isinstance(other, _actual_datetime.timedelta):
            o = self.toordinal() + other.days
            if 0 < o <= _MAXORDINAL:
                return date.fromordinal(o)
            raise OverflowError("result out of range")
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        """Subtract two nepali_datetime.date objects.

        Parameters
        ----------
        other: datetime.timedelta
            The other object to which the self is subtracted from.

        Returns
        -------
        nepali_datetime.date
            The new nepali_datetime.date object after subtraction operation.
        """
        if isinstance(other, _actual_datetime.timedelta):
            return self + _actual_datetime.timedelta(-other.days)
        if isinstance(other, date):
            days1 = self.toordinal()
            days2 = other.toordinal()
            return _actual_datetime.timedelta(days1 - days2)
        return NotImplemented

    def weekday(self):
        """Return day of the week, where Sunday == 0 ... Saturday == 6."""
        return (self.toordinal() + 5) % 7

    def isoweekday(self):
        return NotImplemented

    def isocalendar(self):
        return NotImplemented

    def _getstate(self):
        return NotImplemented

    def __setstate(self, string):
        return NotImplemented

    def __reduce__(self):
        return NotImplemented


_date_class = date  # so functions w/ args named "date" can get at the class

date.min = date(**MINDATE)
date.max = date(**MAXDATE)
date.resolution = _actual_datetime.timedelta(days=1)


class datetime(date):
    """datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])

    The year, month and day arguments are required. tzinfo may be None, or an
    instance of a tzinfo subclass. The remaining arguments may be ints.
    """
    __slots__ = date.__slots__ + ('_hour', '_minute', '_second', '_microsecond', '_tzinfo', '_hashcode')

    def __new__(cls, year, month=None, day=None, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
        year, month, day = _check_date_fields(year, month, day)
        hour, minute, second, microsecond = _check_time_fields(hour, minute, second, microsecond)
        _check_tzinfo_arg(tzinfo)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = UTC0545() if tzinfo is None else tzinfo
        self._hashcode = -1
        return self

    @property
    def hour(self):
        """hour (0-23)"""
        return self._hour

    @property
    def minute(self):
        """minute (0-59)"""
        return self._minute

    @property
    def second(self):
        """second (0-59)"""
        return self._second

    @property
    def microsecond(self):
        """microsecond (0-999999)"""
        return self._microsecond

    @property
    def tzinfo(self):
        """timezone info object"""
        return self._tzinfo

    @classmethod
    def _fromtimestamp(cls, t, utc, tz):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """
        frac, t = _math.modf(t)
        us = round(frac * 1e6)
        if us >= 1000000:
            t += 1
            us -= 1000000
        elif us < 0:
            t -= 1
            us += 1000000

        converter = _time.gmtime if utc else _time.localtime
        y, m, d, hh, mm, ss, weekday, jday, dst = converter(t)
        dt = super().from_datetime_date(_actual_datetime.date(y, m, d))
        y, m, d = dt.year, dt.month, dt.day
        ss = min(ss, 59)  # clamp out leap seconds if the platform has them
        return cls(y, m, d, hh, mm, ss, us, tz)

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        """Construct a datetime from a POSIX timestamp (like time.time()).

        A timezone info object may be passed in as well.
        """
        _check_tzinfo_arg(tz)

        result = cls._fromtimestamp(t, tz is not None, tz)
        if tz is not None:
            result = tz.fromutc(result)
        return result

    @classmethod
    def utcfromtimestamp(cls, t):
        """Construct a naive UTC datetime from a POSIX timestamp."""
        return cls._fromtimestamp(t, True, None)

    @classmethod
    def now(cls):
        """Construct a datetime from time.time() and optional time zone info."""
        t = _time.time()
        return cls.fromtimestamp(t, UTC0545())

    @classmethod
    def utcnow(cls):
        """Construct a UTC datetime from time.time()."""
        t = _time.time()
        return cls.utcfromtimestamp(t)

    @classmethod
    def combine(cls, date, time):
        """Construct a datetime from a given date and a given time."""
        if not isinstance(date, _date_class):
            raise TypeError("date argument must be a date instance")
        if not isinstance(time, _actual_datetime.time):
            raise TypeError("time argument must be a time instance")
        return cls(
            date.year, date.month, date.day,
            time.hour, time.minute, time.second, time.microsecond,
            time.tzinfo
        )

    def timetuple(self):
        """Return local time tuple compatible with time.localtime()."""
        dst = self.dst()
        if dst is None:
            dst = -1
        elif dst:
            dst = 1
        else:
            dst = 0
        return _build_struct_time(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second,
            dst
        )

    @classmethod
    def from_datetime_datetime(cls, from_datetime):
        """Convert datetime.date to nepali_datetime.datetime (A.D datetime to B.S).

        Parameters
        ----------
        from_date: datetime.datetime
            The AD datetime object to be converted.

        Returns
        -------
        nepali_datetime.datetime
            The converted nepali_datetime.datetime object.
        """
        from_datetime = from_datetime.astimezone(UTC0545())
        return cls.combine(cls.from_datetime_date(from_datetime.date()), from_datetime.time())

    def to_datetime_datetime(self):
        """Convert nepali_datetime.datetime to datetime.datetime (B.S datetime to A.D).

        Returns
        -------
        datetime.datetime
            The converted datetime.datetime object.
        """
        return _actual_datetime.datetime.fromtimestamp(self.timestamp())

    def _mktime(self):
        """Return integer POSIX timestamp."""
        max_fold_seconds = 24 * 3600
        t = (self - _EPOCH_BS) // _actual_datetime.timedelta(0, 1)

        def local(u):
            y, m, d, hh, mm, ss = _time.localtime(u)[:6]
            return (datetime(y, m, d, hh, mm, ss) - _EPOCH_BS) // _actual_datetime.timedelta(0, 1)

        # Our goal is to solve t = local(u) for u.
        a = local(t) - t
        u1 = t - a
        t1 = local(u1)
        if t1 == t:
            # We found one solution, but it may not be the one we need.
            # Look for an earlier solution (if `fold` is 0), or a
            # later one (if `fold` is 1).
            u2 = u1 + (-max_fold_seconds, max_fold_seconds)[self.fold]
            b = local(u2) - u2
            if a == b:
                return u1
        else:
            b = t1 - u1
            assert a != b
        u2 = t - b
        t2 = local(u2)
        if t2 == t:
            return u2
        if t1 == t:
            return u1
        # We have found both offsets a and b, but neither t - a nor t - b is
        # a solution.  This means t is in the gap.
        return (max, min)[self.fold](u1, u2)

    def timestamp(self):
        """Return POSIX timestamp as float"""
        if self._tzinfo is None:
            s = self._mktime()
            return s + self.microsecond / 1e6
        else:
            return (self - _EPOCH_BS).total_seconds()

    def utctimetuple(self):
        """Return UTC time tuple compatible with time.gmtime()."""
        offset = self.utcoffset()
        if offset:
            self -= offset
        y, m, d = self.year, self.month, self.day
        hh, mm, ss = self.hour, self.minute, self.second
        return _build_struct_time(y, m, d, hh, mm, ss, 0)

    def date(self):
        """Return the date part."""
        return date(self._year, self._month, self._day)

    def time(self):
        """Return the time part, with tzinfo None."""
        return _actual_datetime.time(self.hour, self.minute, self.second, self.microsecond)

    def timetz(self):
        """Return the time part, with same tzinfo."""
        return _actual_datetime.time(self.hour, self.minute, self.second, self.microsecond, self._tzinfo)

    def replace(self, year=None, month=None, day=None, hour=None,
                minute=None, second=None, microsecond=None, tzinfo=True):
        """Return a new datetime with new values for the specified fields."""
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond
        if tzinfo is True:
            tzinfo = self.tzinfo
        return datetime(year, month, day, hour, minute, second, microsecond, tzinfo)

    def astimezone(self, tz=None):
        if tz is None:
            tz = UTC0545()
        elif not isinstance(tz, _actual_datetime.tzinfo):
            raise TypeError("tz argument must be an instance of tzinfo")

        mytz = self.tzinfo
        if mytz is None:
            mytz = self._local_timezone()
            myoffset = mytz.utcoffset(self)
        else:
            myoffset = mytz.utcoffset(self)
            if myoffset is None:
                mytz = self.replace(tzinfo=None)._local_timezone()
                myoffset = mytz.utcoffset(self)

        if tz is mytz:
            return self

        utc = (self - myoffset).replace(tzinfo=tz)

        return tz.fromutc(utc)

    def ctime(self):
        """Return ctime() style string."""
        weekday = (self.toordinal() + 5) % 7 or 7
        return "%s %s %2d %02d:%02d:%02d %04d" % (
            _DAYNAMES[weekday],
            _MONTHNAMES[self._month],
            self._day,
            self._hour, self._minute, self._second,
            self._year
        )

    def isoformat(self, sep='T'):
        """Return the time formatted according to ISO.

        This is 'YYYY-MM-DD HH:MM:SS.mmmmmm', or 'YYYY-MM-DD HH:MM:SS' if
        self.microsecond == 0.

        If self.tzinfo is not None, the UTC offset is also attached, giving
        'YYYY-MM-DD HH:MM:SS.mmmmmm+HH:MM' or 'YYYY-MM-DD HH:MM:SS+HH:MM'.

        Optional argument sep specifies the separator between date and
        time, default 'T'.
        """
        s = (
                "%04d-%02d-%02d%c" % (self._year, self._month, self._day, sep) +
                _format_time(self._hour, self._minute, self._second, self._microsecond)
        )
        off = self.utcoffset()
        if off is not None:
            if off.days < 0:
                sign = "-"
                off = -off
            else:
                sign = "+"
            hh, mm = divmod(off, _actual_datetime.timedelta(hours=1))
            assert not mm % _actual_datetime.timedelta(minutes=1), "whole minute"
            mm //= _actual_datetime.timedelta(minutes=1)
            s += "%s%02d:%02d" % (sign, hh, mm)
        return s

    def __repr__(self):
        """Convert to formal string, for repr()."""
        L = [self._year, self._month, self._day,  # These are never zero
             self._hour, self._minute, self._second, self._microsecond]
        if L[-1] == 0:
            del L[-1]
        if L[-1] == 0:
            del L[-1]
        s = "%s.%s(%s)" % (self.__class__.__module__,
                           self.__class__.__qualname__,
                           ", ".join(map(str, L)))
        if self._tzinfo is not None:
            assert s[-1:] == ")"
            s = s[:-1] + ", tzinfo=%r" % self._tzinfo + ")"
        return s

    def __str__(self):
        """Convert to string, for str()."""
        return self.isoformat(sep=' ')

    @classmethod
    def strptime(cls, date_string, format):
        """string, format -> new datetime parsed from a string (like time.strptime())."""
        from . import _custom_strptime
        return _custom_strptime._strptime_datetime(cls, date_string, format)

    def utcoffset(self):
        """Return the timezone offset in minutes east of UTC (negative west of UTC)."""
        if self._tzinfo is None:
            return None
        offset = self._tzinfo.utcoffset(self)
        _check_utc_offset("utcoffset", offset)
        return offset

    def tzname(self):
        """Return the timezone name.

        Note that the name is 100% informational -- there's no requirement that
        it mean anything in particular. For example, "GMT", "UTC", "-500",
        "-5:00", "EDT", "US/Eastern", "America/New York" are all valid replies.
        """
        if self._tzinfo is None:
            return None
        name = self._tzinfo.tzname(self)
        _check_tzname(name)
        return name

    def dst(self):
        """Return 0 if DST is not in effect, or the DST offset (in minutes
        eastward) if DST is in effect.

        This is purely informational; the DST offset has already been added to
        the UTC offset returned by utcoffset() if applicable, so there's no
        need to consult dst() unless you're interested in displaying the DST
        info.
        """
        if self._tzinfo is None:
            return None
        offset = self._tzinfo.dst(self)
        _check_utc_offset("dst", offset)
        return offset

    def __eq__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other, allow_mixed=True) == 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            return False

    def __le__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) <= 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            _cmperror(self, other)

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) < 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            _cmperror(self, other)

    def __ge__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) >= 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            _cmperror(self, other)

    def __gt__(self, other):
        if isinstance(other, datetime):
            return self._cmp(other) > 0
        elif not isinstance(other, date):
            return NotImplemented
        else:
            _cmperror(self, other)

    def _cmp(self, other, allow_mixed=False):
        assert isinstance(other, datetime)
        mytz = self._tzinfo
        ottz = other._tzinfo
        myoff = otoff = None

        if mytz is ottz:
            base_compare = True
        else:
            myoff = self.utcoffset()
            otoff = other.utcoffset()
            base_compare = myoff == otoff

        if base_compare:
            return _cmp((self._year, self._month, self._day,
                         self._hour, self._minute, self._second,
                         self._microsecond),
                        (other._year, other._month, other._day,
                         other._hour, other._minute, other._second,
                         other._microsecond))
        if myoff is None or otoff is None:
            if allow_mixed:
                return 2  # arbitrary non-zero value
            else:
                raise TypeError("cannot compare naive and aware datetimes")
        # XXX What follows could be done more efficiently...
        diff = self - other  # this will take offsets into account
        if diff.days < 0:
            return -1
        return diff and 1 or 0

    def __add__(self, other):
        """Add a datetime and a timedelta."""
        if not isinstance(other, _actual_datetime.timedelta):
            return NotImplemented
        delta = _actual_datetime.timedelta(
            self.toordinal(),
            hours=self._hour,
            minutes=self._minute,
            seconds=self._second,
            microseconds=self._microsecond
        )
        delta += other
        hour, rem = divmod(delta.seconds, 3600)
        minute, second = divmod(rem, 60)
        if 0 < delta.days <= _MAXORDINAL:
            return datetime.combine(
                date.fromordinal(delta.days),
                _actual_datetime.time(hour, minute, second, delta.microseconds, tzinfo=self._tzinfo)
            )
        raise OverflowError("result out of range")

    __radd__ = __add__

    def __sub__(self, other):
        """Subtract two datetimes, or a datetime and a timedelta."""
        if not isinstance(other, datetime):
            if isinstance(other, _actual_datetime.timedelta):
                return self + -other
            return NotImplemented

        days1 = self.toordinal()
        days2 = other.toordinal()
        secs1 = self._second + self._minute * 60 + self._hour * 3600
        secs2 = other._second + other._minute * 60 + other._hour * 3600
        base = _actual_datetime.timedelta(days1 - days2, secs1 - secs2, self._microsecond - other._microsecond)
        if self._tzinfo is other._tzinfo:
            return base
        myoff = self.utcoffset()
        otoff = other.utcoffset()
        if myoff == otoff:
            return base
        if myoff is None or otoff is None:
            raise TypeError("cannot mix naive and timezone-aware time")
        return base + otoff - myoff

    def __hash__(self):
        return NotImplemented

    def _getstate(self):
        return NotImplemented

    def __setstate(self, string, tzinfo):
        return NotImplemented

    def __reduce__(self):
        return NotImplemented


datetime.min = datetime(1975, 1, 1)
datetime.max = datetime(2100, 12, 30, 23, 59, 59, 999999)
datetime.resolution = _actual_datetime.timedelta(microseconds=1)

_EPOCH_BS = datetime.from_datetime_datetime(_actual_datetime.datetime(1970, 1, 1, tzinfo=_actual_datetime.timezone.utc))
