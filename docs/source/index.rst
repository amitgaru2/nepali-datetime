.. nepali_datetime documentation master file, created by
   sphinx-quickstart on Sat Jul 18 13:35:34 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:mod:`nepali_datetime` --- Bikram Sambat Date and Nepal Time types
================================================================================
.. module:: nepali_datetime
   :synopsis: Basic date and time types that operates on B.S .

.. moduleauthor:: Amit Garu <amitgaru2@gmail.com>
.. sectionauthor:: Amit Garu <amitgaru2@gmail.com>

The :mod:`nepali_datetime` module is highly motivated from the Python3's 
:mod:`datetime` module. The module supplies classes for manipulating 
Bikram Sambat dates and Nepal times in both simple and complex ways.


The :mod:`nepali_datetime` module exports the following constants:

.. data:: MINYEAR
   
   The smallest year number allowed in a :class:`date` or :class:`.datetime` object. :const:`MINYEAR` is ``1975``.

.. data:: MAXYEAR
   
   The largest year number allowed in a :class:`date` or :class:`.datetime` object. :const:`MAXYEAR` is ``2100``.

.. data:: NEPAL_TIME_UTC_OFFSET

   The UTC offset of Nepal time ``+05:45``.

Available Types
---------------

.. class:: date
   :noindex:

   An idealized naive date, assuming the current Gregorian calendar always was, and
   always will be, in effect. Attributes: :attr:`year`, :attr:`month`, and
   :attr:`day`.

.. class:: UTC0545

   A :class:`tzinfo` subclass for Nepal timezone.


.. class:: datetime
   :noindex:

   A combination of a date and a time. Attributes: :attr:`year`, :attr:`month`,
   :attr:`day`, :attr:`hour`, :attr:`minute`, :attr:`second`, :attr:`microsecond`,
   and :attr:`.tzinfo`.


:class:`nepali_datetime.date` Objects
-------------------------------------

A :class:`date` object represents a date (year, month and day) in B.S calendar.  Baishak 1 of year 1975 is called day
number 1, Baishak 2 of year 1975 is called day number 2, and so on.

.. class:: date(year, month, day)

   All arguments are required.  Arguments may be integers, in the following
   ranges:

   * ``MINYEAR <= year <= MAXYEAR``
   * ``1 <= month <= 12``
   * ``1 <= day <= number of days in the given month and year``

   If an argument outside those ranges is given, :exc:`ValueError` is raised.


Other constructors, all class methods:

.. classmethod:: date.today()

   Return the current B.S date.


.. classmethod:: date.from_datetime_date(datetime.date)

   Return the converted :class:`nepalidatetime.date` (B.S) object for the given ``datetime.date`` object.

   Example::

      >>> import datetime
      >>> import nepali_datetime
      >>> dt = datetime.date(2018, 11, 7)
      >>> nepali_datetime.date.from_datetime_date(dt)
      nepali_datetime.date(2075, 7, 21)

Class attributes:

.. attribute:: date.min

   The earliest representable date, ``date(MINYEAR, 1, 1)``.


.. attribute:: date.max

   The latest representable date, ``date(MAXYEAR, 12, MAXYEAR_LAST_MONTHS_LAST_DAY)``.


.. attribute:: date.resolution

   The smallest possible difference between non-equal date objects,
   ``timedelta(days=1)``.


Instance attributes (read-only):

.. attribute:: date.year

   Between :const:`MINYEAR` and :const:`MAXYEAR` inclusive.


.. attribute:: date.month

   Between 1 and 12 inclusive.


.. attribute:: date.day

   Between 1 and the number of days in the given month of the given year.


Supported operations:

+-------------------------------+----------------------------------------------+
| Operation                     | Result                                       |
+===============================+==============================================+
| ``date2 = date1 + timedelta`` | *date2* is ``timedelta.days`` days removed   |
|                               | from *date1*.  (1)                           |
+-------------------------------+----------------------------------------------+
| ``date2 = date1 - timedelta`` | Computes *date2* such that ``date2 +         |
|                               | timedelta == date1``. (2)                    |
+-------------------------------+----------------------------------------------+
| ``timedelta = date1 - date2`` | \(3)                                         |
+-------------------------------+----------------------------------------------+
| ``date1 < date2``             | *date1* is considered less than *date2* when |
|                               | *date1* precedes *date2* in time. (4)        |
+-------------------------------+----------------------------------------------+

Notes:

(1)
   *date2* is moved forward in time if ``timedelta.days > 0``, or backward if
   ``timedelta.days < 0``.  Afterward ``date2 - date1 == timedelta.days``.
   ``timedelta.seconds`` and ``timedelta.microseconds`` are ignored.
   :exc:`OverflowError` is raised if ``date2.year`` would be smaller than
   :const:`MINYEAR` or larger than :const:`MAXYEAR`.

(2)
   This isn't quite equivalent to date1 + (-timedelta), because -timedelta in
   isolation can overflow in cases where date1 - timedelta does not.
   ``timedelta.seconds`` and ``timedelta.microseconds`` are ignored.

(3)
   This is exact, and cannot overflow.  timedelta.seconds and
   timedelta.microseconds are 0, and date2 + timedelta == date1 after.

(4)
   In other words, ``date1 < date2`` if and only if ``date1.toordinal() <
   date2.toordinal()``. In order to stop comparison from falling back to the
   default scheme of comparing object addresses, date comparison normally raises
   :exc:`TypeError` if the other comparand isn't also a :class:`date` object.
   However, ``NotImplemented`` is returned instead if the other comparand has a
   :meth:`timetuple` attribute.  This hook gives other kinds of date objects a
   chance at implementing mixed-type comparison. If not, when a :class:`date`
   object is compared to an object of a different type, :exc:`TypeError` is raised
   unless the comparison is ``==`` or ``!=``.  The latter cases return
   :const:`False` or :const:`True`, respectively.


Instance methods:

.. method:: date.replace(year, month, day)

   Return a date with the same value, except for those parameters given new
   values by whichever keyword arguments are specified.  For example, if ``d ==
   date(2002, 12, 30)``, then ``d.replace(day=26) == date(2002, 12, 26)``.


.. method:: date.timetuple()

   Return a :class:`time.struct_time` such as returned by :func:`time.localtime`.
   The hours, minutes and seconds are 0, and the DST flag is -1. ``d.timetuple()``
   is equivalent to ``time.struct_time((d.year, d.month, d.day, 0, 0, 0,
   d.weekday(), yday, -1))``, where ``yday = d.toordinal() - date(d.year, 1,
   1).toordinal() + 1`` is the day number within the current year starting with
   ``1`` for Baishak 1st.


.. method:: date.weekday()

   Return the day of the week as an integer, where Sunday is 0 and Saturday is 6.
   For example, ``date(2002, 12, 4).weekday() == 0``, a Sunday.


.. method:: date.to_datetime_date()

   Return the converted ``datetime.date`` (A.D) object of the :class:`nepali_datetime.date` object.

   Example::

      >>> import nepali_datetime
      >>> ndt = nepali_datetime.date(2075, 7, 21)
      >>> ndt.to_datetime_date()
      datetime.date(2018, 11, 7)

.. method:: date.isoformat()

   Return a string representing the date in ISO 8601 format, 'YYYY-MM-DD'.  For
   example, ``date(2002, 12, 4).isoformat() == '2002-12-04'``.


.. method:: date.__str__()

   For a date *d*, ``str(d)`` is equivalent to ``d.isoformat()``.

.. method:: date.calendar(justify=4)

   Dispaly a B.S calendar for the date object's month with the object's day highlighted. Override 
   default ``justify=4`` for wider view of calendar.

   Example::
   
      >>> import nepali_datetime
      >>> ndt = nepali_datetime.date(2051, 10, 1)
      >>> ndt.calendar()

                      Magh 2051                 
         Sun   Mon   Tue   Wed   Thu   Fri   Sat
           1     2     3     4     5     6     7
           8     9    10    11    12    13    14
          15    16    17    18    19    20    21
          22    23    24    25    26    27    28
          29


.. method:: date.ctime()

   Return a string representing the date, for example ``date(2002, 12,
   4).ctime() == 'Wed Cha 4 00:00:00 2002'``. ``d.ctime()`` is equivalent to
   ``time.ctime(time.mktime(d.timetuple()))`` on platforms where the native C
   :c:func:`ctime` function (which :func:`time.ctime` invokes, but which
   :meth:`date.ctime` does not invoke) conforms to the C standard.


.. method:: date.strftime(format)

   Return a string representing the date, controlled by an explicit format string.
   Format codes referring to hours, minutes or seconds will see 0 values. For a
   complete list of formatting directives, see
   :ref:`strftime-strptime-behavior`.


.. method:: date.__format__(format)

   Same as :meth:`.date.strftime`. This makes it possible to specify a format
   string for a :class:`.date` object when using :meth:`str.format`. For a
   complete list of formatting directives, see
   :ref:`strftime-strptime-behavior`.


Example of counting days to an event::

    >>> import time
    >>> import nepali_datetime
    >>> today = nepali_datetime.date.today()
    >>> today
    nepali_datetime.date(2050, 12, 5)
    >>> today == nepali_datetime.date.fromtimestamp(time.time())
    True
    >>> my_birthday = nepali_datetime.date(today.year, 10, 1)
    >>> if my_birthday < today:
    ...     my_birthday = my_birthday.replace(year=today.year + 1)
    >>> my_birthday
    nepali_datetime.date(2051, 10, 1)
    >>> time_to_birthday = abs(my_birthday - today)
    >>> time_to_birthday.days
    303

Example of working with :class:`date`:

.. doctest::

    >>> import nepali_datetime
    >>> d = nepali_datetime.date.fromordinal(10000) # 10000th day after 1. 1. 1975
    >>> d
    nepali_datetime.date(2002, 5, 12)
    >>> d.isoformat()
    '2002-05-12'
    >>> d.strftime("%d/%m/%y")
    '12/05/02'
    >>> d.strftime("%A %d. %B %Y")
    'Tuesday 12. Bhadau 2002'
    >>> 'The {1} is {0:%d}, the {2} is {0:%B}.'.format(d, "day", "month")
    'The day is 12, the month is Bhadau.'

:class:`nepali_datetime.datetime` Objects
-----------------------------------------

A :class:`datetime` object is a single object containing all the information
from a :class:`date` object and a :class:`time` object.  Like a :class:`date`
object, :class:`datetime` assumes the current Gregorian calendar extended in
both directions; like a time object, :class:`datetime` assumes there are exactly
3600\*24 seconds in every day.

Constructor:

.. class:: datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

   The year, month and day arguments are required.  *tzinfo* may be ``None``, or an
   instance of a :class:`UTC0545`.  The remaining arguments may be integers,
   in the following ranges:

   * ``MINYEAR <= year <= MAXYEAR``
   * ``1 <= month <= 12``
   * ``1 <= day <= number of days in the given month and year``
   * ``0 <= hour < 24``
   * ``0 <= minute < 60``
   * ``0 <= second < 60``
   * ``0 <= microsecond < 1000000``

   If an argument outside those ranges is given, :exc:`ValueError` is raised.

Other constructors, all class methods:

.. classmethod:: datetime.today()

   Return the current B.S datetime, with :attr:`.tzinfo` as :class:`.UTC0545` instance.


.. classmethod:: datetime.now()

   Return the current local date and time.  If optional argument *tz* is ``None``
   or not specified, this is like :meth:`today`, but, if possible, supplies more
   precision than can be gotten from going through a :func:`time.time` timestamp
   (for example, this may be possible on platforms supplying the C
   :c:func:`gettimeofday` function).

   The *tz* is explicitly set to restrict to Nepal timezone which is an instance
   of :class:`.UTC0545`. See also :meth:`today`, :meth:`utcnow`.


.. classmethod:: datetime.utcnow()

   Return the current UTC date and time, with :attr:`.tzinfo` ``None``. This is like
   :meth:`now`, but returns the current UTC date and time, as a naive
   :class:`.datetime` object. See also :meth:`now`.


.. classmethod:: datetime.strptime(date_string, format)

   Return a :class:`.datetime` corresponding to *date_string*, parsed according to
   *format*.  This is equivalent to ``datetime(*(time.strptime(date_string,
   format)[0:6]))``. :exc:`ValueError` is raised if the date_string and format
   can't be parsed by :func:`time.strptime` or if it returns a value which isn't a
   time tuple. For a complete list of formatting directives, see
   :ref:`strftime-strptime-behavior`.



Class attributes:

.. attribute:: datetime.min

   The earliest representable :class:`.datetime`, ``datetime(MINYEAR, 1, 1,
   tzinfo=None)``.


.. attribute:: datetime.max

   The latest representable :class:`.datetime`, ``datetime(MAXYEAR, 12, MAXYEAR_LAST_MONTHS_LAST_DAY, 23, 59,
   59, 999999, tzinfo=None)``.


.. attribute:: datetime.resolution

   The smallest possible difference between non-equal :class:`.datetime` objects,
   ``timedelta(microseconds=1)``.


Instance attributes (read-only):

.. attribute:: datetime.year

   Between :const:`MINYEAR` and :const:`MAXYEAR` inclusive.


.. attribute:: datetime.month

   Between 1 and 12 inclusive.


.. attribute:: datetime.day

   Between 1 and the number of days in the given month of the given year.


.. attribute:: datetime.hour

   In ``range(24)``.


.. attribute:: datetime.minute

   In ``range(60)``.


.. attribute:: datetime.second

   In ``range(60)``.


.. attribute:: datetime.microsecond

   In ``range(1000000)``.


.. attribute:: datetime.tzinfo

   The object passed as the *tzinfo* argument to the :class:`.datetime` constructor,
   or ``None`` if none was passed.


Supported operations:

+---------------------------------------+--------------------------------+
| Operation                             | Result                         |
+=======================================+================================+
| ``datetime2 = datetime1 + timedelta`` | \(1)                           |
+---------------------------------------+--------------------------------+
| ``datetime2 = datetime1 - timedelta`` | \(2)                           |
+---------------------------------------+--------------------------------+
| ``timedelta = datetime1 - datetime2`` | \(3)                           |
+---------------------------------------+--------------------------------+
| ``datetime1 < datetime2``             | Compares :class:`.datetime` to |
|                                       | :class:`.datetime`. (4)        |
+---------------------------------------+--------------------------------+

(1)
   datetime2 is a duration of timedelta removed from datetime1, moving forward in
   time if ``timedelta.days`` > 0, or backward if ``timedelta.days`` < 0.  The
   result has the same :attr:`~.datetime.tzinfo` attribute as the input datetime, and
   datetime2 - datetime1 == timedelta after. :exc:`OverflowError` is raised if
   datetime2.year would be smaller than :const:`MINYEAR` or larger than
   :const:`MAXYEAR`. Note that no time zone adjustments are done even if the
   input is an aware object.

(2)
   Computes the datetime2 such that datetime2 + timedelta == datetime1. As for
   addition, the result has the same :attr:`~.datetime.tzinfo` attribute as the input
   datetime, and no time zone adjustments are done even if the input is aware.
   This isn't quite equivalent to datetime1 + (-timedelta), because -timedelta
   in isolation can overflow in cases where datetime1 - timedelta does not.

(3)
   Subtraction of a :class:`.datetime` from a :class:`.datetime` is defined only if
   both operands are naive, or if both are aware.  If one is aware and the other is
   naive, :exc:`TypeError` is raised.

   If both are naive, or both are aware and have the same :attr:`~.datetime.tzinfo` attribute,
   the :attr:`~.datetime.tzinfo` attributes are ignored, and the result is a :class:`timedelta`
   object *t* such that ``datetime2 + t == datetime1``.  No time zone adjustments
   are done in this case.

   If both are aware and have different :attr:`~.datetime.tzinfo` attributes, ``a-b`` acts
   as if *a* and *b* were first converted to naive UTC datetimes first.  The
   result is ``(a.replace(tzinfo=None) - a.utcoffset()) - (b.replace(tzinfo=None)
   - b.utcoffset())`` except that the implementation never overflows.

(4)
   *datetime1* is considered less than *datetime2* when *datetime1* precedes
   *datetime2* in time.

   If one comparand is naive and the other is aware, :exc:`TypeError`
   is raised if an order comparison is attempted.  For equality
   comparisons, naive instances are never equal to aware instances.

   If both comparands are aware, and have the same :attr:`~.datetime.tzinfo` attribute, the
   common :attr:`~.datetime.tzinfo` attribute is ignored and the base datetimes are
   compared.  If both comparands are aware and have different :attr:`~.datetime.tzinfo`
   attributes, the comparands are first adjusted by subtracting their UTC
   offsets (obtained from ``self.utcoffset()``).


Instance methods:

.. method:: datetime.date()

   Return :class:`date` object with same year, month and day.


.. method:: datetime.time()

   Return :class:`time` object with same hour, minute, second and microsecond.
   :attr:`.tzinfo` is ``None``.  See also method :meth:`timetz`.


.. method:: datetime.timetz()

   Return :class:`time` object with same hour, minute, second, microsecond, and
   tzinfo attributes.  See also method :meth:`time`.


.. method:: datetime.replace([year[, month[, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]]]]])

   Return a datetime with the same attributes, except for those attributes given
   new values by whichever keyword arguments are specified.  Note that
   ``tzinfo=None`` can be specified to create a naive datetime from an aware
   datetime with no conversion of date and time data.


.. method:: datetime.tzname()

   If :attr:`.tzinfo` is ``None``, returns ``None``, else returns
   ``self.tzinfo.tzname(self)``, raises an exception if the latter doesn't return
   ``None`` or a string object,


.. method:: datetime.timetuple()

   Return a :class:`time.struct_time` such as returned by :func:`time.localtime`.
   ``d.timetuple()`` is equivalent to ``time.struct_time((d.year, d.month, d.day,
   d.hour, d.minute, d.second, d.weekday(), yday, dst))``, where ``yday =
   d.toordinal() - date(d.year, 1, 1).toordinal() + 1`` is the day number within
   the current year starting with ``1`` for Baishak 1st. The :attr:`tm_isdst` flag
   of the result is set according to the :meth:`dst` method: :attr:`.tzinfo` is
   ``None`` or :meth:`dst` returns ``None``, :attr:`tm_isdst` is set to ``-1``;
   else if :meth:`dst` returns a non-zero value, :attr:`tm_isdst` is set to ``1``;
   else :attr:`tm_isdst` is set to ``0``.


.. method:: datetime.weekday()

   Return the day of the week as an integer, where Sunday is 0 and Saturday is 6.
   The same as ``self.date().weekday()``. See also :meth:`isoweekday`.


.. method:: datetime.isoformat(sep='T')


.. method:: datetime.__str__()

   For a :class:`.datetime` instance *d*, ``str(d)`` is equivalent to
   ``d.isoformat(' ')``.


.. method:: datetime.strftime(format)

   Return a string representing the date and time, controlled by an explicit format
   string.  For a complete list of formatting directives, see
   :ref:`strftime-strptime-behavior`.


.. method:: datetime.__format__(format)

   Same as :meth:`.datetime.strftime`.  This makes it possible to specify a format
   string for a :class:`.datetime` object when using :meth:`str.format`.  For a
   complete list of formatting directives, see
   :ref:`strftime-strptime-behavior`.


Examples of working with datetime objects:

.. doctest::

    >>> import nepali_datetime
    >>> # Using datetime.combine()
    >>> d = nepali_datetime.date(2005, 7, 14)
    >>> t = time(12, 30)
    >>> nepali_datetime.datetime.combine(d, t)
    nepali_datetime.datetime(2005, 7, 14, 12, 30)
    >>> # Using nepali_datetime.datetime.now() or nepali_datetime.datetime.utcnow()
    >>> nepali_datetime.datetime.now()   # doctest: +SKIP
    nepali_datetime.datetime(2007, 12, 6, 16, 30, 43, 79043)   # GMT +5:45
    >>> nepali_datetime.datetime.utcnow()   # doctest: +SKIP
    nepali_datetime.datetime(2007, 12, 6, 10, 45, 43, 79060)
    >>> # Using nepali_datetime.datetime.strptime()
    >>> dt = nepali_datetime.datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
    >>> dt
    nepali_datetime.datetime(2006, 11, 21, 16, 30)
    >>> # Formatting datetime
    >>> dt.strftime("%A, %d. %B %Y %I:%M%p")
    'Saturday, 21. Falgun 2006 04:30PM'
    >>> 'The {1} is {0:%d}, the {2} is {0:%B}, the {3} is {0:%I:%M%p}.'.format(dt, "day", "month", "time")
    'The day is 21, the month is Falgun, the time is 04:30PM.'


.. _strftime-strptime-behavior:

:meth:`strftime` and :meth:`strptime` Behavior
----------------------------------------------

:class:`date`, :class:`.datetime`, and :class:`time` objects all support a
``strftime(format)`` method, to create a string representing the time under the
control of an explicit format string.  Broadly speaking, ``d.strftime(fmt)``
acts like the :mod:`time` module's ``time.strftime(fmt, d.timetuple())``
although not all objects support a :meth:`timetuple` method.

Conversely, the :meth:`datetime.strptime` class method creates a
:class:`.datetime` object from a string representing a date and time and a
corresponding format string. ``datetime.strptime(date_string, format)`` is
equivalent to ``datetime(*(time.strptime(date_string, format)[0:6]))``.

For :class:`time` objects, the format codes for year, month, and day should not
be used, as time objects have no such values.  If they're used anyway, ``1975``
is substituted for the year, and ``1`` for the month and day.

For :class:`date` objects, the format codes for hours, minutes, seconds, and
microseconds should not be used, as :class:`date` objects have no such
values.  If they're used anyway, ``0`` is substituted for them.

The following is a list of all the format codes that the C standard (1989
version) requires, and these work on all platforms with a standard C
implementation.  Note that the 1999 version of the C standard added additional
format codes.


===========  ================================ ======================== =======
Directives   Meaning                          Example                  Notes
===========  ================================ ======================== =======
``%a``       Weekday as locale's              Sun, Mon, ..., Sat       \(1)
             abbreviated name.                                

``%A``       Weekday as locale's full name.   Sunday, Monday, ...,     \(1)  
                                              Saturday                     
                                                                          
``%G``       Weekday as locale's full name    आइतबार, सोमबार, ...,       \(1)  
             in Nepali unicode.               शनिबार                     

``%w``       Weekday as a decimal number,     0, 1, ..., 6                  
             where 0 is Sunday and 6 is                                    
             Saturday.                         

``%d``       Day of the month as a            01, 02, ..., 32               
             zero-padded decimal number.                                   

``%D``       Day of the month as a            ०१, ०२, ..., ३२               
             zero-padded decimal number      
             in Nepali unicode.

``%b``       Month as locale's abbreviated    Bai, Jes, ..., Cha       \(1)  
             name.                                                         
                                                                                                                                                  
``%B``       Month as locale's full name.     Baishakh, Jestha,        \(1)  
                                              ..., Chaitra                                                                                                                                                              

``%N``       Month as locale's full name      वैशाख, जेष्ठ, असार,          \(1)
             in Nepali unicode.               श्रावण, भदौ, आश्विन,
                                              कार्तिक, मंसिर, पौष, माघ,
                                              फाल्गुण, चैत्र

``%m``       Month as a zero-padded           01, 02, ..., 12               
             decimal number.                                               

``%y``       Year without century as a        00, 01, ..., 99               
             zero-padded decimal number.
                                   
``%Y``       Year with century as a           1975, 1976, ..., 2020,   \(2) 
             decimal number.                  2021, ..., 2099, 2100         

``%k``       Year without century as a        ००, ०१, ..., ९९               
             zero-padded decimal number
             in Nepali unicode.

``%K``       Year with century as a           १९७५, १९७६, ...,         \(2) 
             decimal number in                २०९९, २१००        
             Nepali unicode.

``%H``       Hour (24-hour clock) as a        00, 01, ..., 23               
             zero-padded decimal number.
                     
``%I``       Hour (12-hour clock) as a        01, 02, ..., 12               
             zero-padded decimal number.                          

``%p``       Locale's equivalent of either    AM, PM                   \(1)
             AM or PM.                                                     

``%M``       Minute as a zero-padded          00, 01, ..., 59               
             decimal number.                                               

``%S``       Second as a zero-padded          00, 01, ..., 59          \(4)  
             decimal number.                                               

``%f``       Microsecond as a decimal         000000, 000001, ...,     \(5)  
             number, zero-padded on the       999999                        
             left.                                                         

``%z``       UTC offset in the form +HHMM     (empty), +0000, -0400,   \(6)  
             or -HHMM (empty string if the    +1030                         
             object is naive).                                             

``%Z``       Time zone name (empty string     (empty), UTC, EST, CST        
             if the object is naive).                                      

===========  ================================ ======================== =======

                        

Notes:

(1)
   Because the format depends on the directive ``%b`` or ``%B`` or ``%N``, care
   should be taken when making assumptions about the output value. Field orderings
   will vary (for example, "month/day/year" versus "day/month/year"), and the output
   may contain Unicode characters.

(2)
   The :meth:`strptime` method can parse years in the full [1, 9999] range, but
   years < 1000 must be zero-filled to 4-digit width.

(3)
   When used with the :meth:`strptime` method, the ``%p`` directive only affects
   the output hour field if the ``%I`` directive is used to parse the hour.

(4)
   Unlike the :mod:`time` module, the :mod:`datetime` module does not support
   leap seconds.

(5)
   When used with the :meth:`strptime` method, the ``%f`` directive
   accepts from one to six digits and zero pads on the right.  ``%f`` is
   an extension to the set of format characters in the C standard (but
   implemented separately in datetime objects, and therefore always
   available).

(6)
   For a naive object, the ``%z`` and ``%Z`` format codes are replaced by empty
   strings.

   For an aware object:

   ``%z``
      :meth:`utcoffset` is transformed into a 5-character string of the form
      +HHMM or -HHMM, where HH is a 2-digit string giving the number of UTC
      offset hours, and MM is a 2-digit string giving the number of UTC offset
      minutes.  For example, if :meth:`utcoffset` returns
      ``timedelta(hours=-3, minutes=-30)``, ``%z`` is replaced with the string
      ``'-0330'``.

   ``%Z``
      If :meth:`tzname` returns ``None``, ``%Z`` is replaced by an empty
      string.  Otherwise ``%Z`` is replaced by the returned value, which must
      be a string.

      When the ``%z`` directive is provided to the :meth:`strptime` method, an
      aware :class:`.datetime` object will be produced.  The ``tzinfo`` of the
      result will be set to a :class:`timezone` instance.
