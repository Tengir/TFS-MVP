from datetime import datetime, timedelta

"""
Два класса DateTime, TimeDelta
Просто обернутые соответсующие классы из импорта.
Чтобы можно было при необходимости заменить библиотеку 
и не менять весь код проекта.
"""


class DateTime:
    def __init__(self, year_or_str=0, month=0, day=0, hour=0, minute=0,
                 second=0,
                 microsecond=0):
        if isinstance(year_or_str, str):
            # Парсим строку в объект timedelta
            try:
                self._datetime = datetime.strptime(year_or_str,
                                                   '%Y-%m-%d %H:%M:%S.%f').replace(
                    tzinfo=None)
            except ValueError:
                raise ValueError(
                    "Некорректный формат строки для создания объекта DateTime") from None
        elif isinstance(year_or_str, int):
            self._datetime = datetime(year_or_str, month, day, hour, minute,
                                      second,
                                      microsecond)
        else:
            raise ValueError(
                "Некорректный 1-ый параметр для создания объекта DateTime")

    @property
    def year(self):
        return self._datetime.year

    @property
    def month(self):
        return self._datetime.month

    @property
    def day(self):
        return self._datetime.day

    @property
    def hour(self):
        return self._datetime.hour

    @property
    def minute(self):
        return self._datetime.minute

    @property
    def second(self):
        return self._datetime.second

    def __str__(self):
        return str(self._datetime)

    def __repr__(self):
        return f"DateTime({self._datetime.year}, {self._datetime.month}, {self._datetime.day}, {self._datetime.hour}, {self._datetime.minute}, {self._datetime.second}, {self._datetime.microsecond})"

    def __add__(self, other):
        if isinstance(other, TimeDelta):
            return DateTime.from_datetime(self._datetime + other._timedelta)
        else:
            raise TypeError(
                "Unsupported operand type(s) for +: 'DateTime' and '{}'".format(
                    type(other)))

    def __sub__(self, other):
        if isinstance(other, DateTime):
            return TimeDelta.from_timedelta(self._datetime - other._datetime)
        elif isinstance(other, TimeDelta):
            return DateTime.from_datetime(self._datetime - other._timedelta)
        else:
            raise TypeError(
                "Unsupported operand type(s) for -: 'DateTime' and '{}'".format(
                    type(other)))

    def __eq__(self, other):
        return self._datetime == other._datetime

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self._datetime > other._datetime

    def __lt__(self, other):
        return self._datetime < other._datetime

    def __ge__(self, other):
        return self._datetime >= other._datetime

    def __le__(self, other):
        return self._datetime <= other._datetime

    @classmethod
    def from_datetime(cls, dt):
        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second,
                   dt.microsecond)


class TimeDelta:
    def __init__(self, day=0, hour=0, minute=0, second=0,
                 microsecond=0):
        total_microseconds = microsecond + 1000000 * (
                second + 60 * (minute + 60 * (hour + 24 * day)))
        self._timedelta = timedelta(microseconds=total_microseconds)

    def __str__(self):
        return str(self._timedelta)

    def __repr__(self):
        return f"TimeDelta(year={self.years}, month={self.months}, day={self.days}, hour={self.hours}, minute={self.minutes}, second={self.seconds}, microsecond={self.microseconds})"

    def __add__(self, other):
        if isinstance(other, TimeDelta):
            return TimeDelta.from_timedelta(self._timedelta + other._timedelta)
        else:
            raise TypeError(
                "Unsupported operand type(s) for +: 'TimeDelta' and '{}'".format(
                    type(other)))

    def __sub__(self, other):
        if isinstance(other, TimeDelta):
            return TimeDelta.from_timedelta(self._timedelta - other._timedelta)
        else:
            raise TypeError(
                "Unsupported operand type(s) for -: 'TimeDelta' and '{}'".format(
                    type(other)))

    def __floordiv__(self, other):
        if isinstance(other, (int, float)):
            total_seconds = self._timedelta.total_seconds()
            divided_seconds = total_seconds // other
            return TimeDelta.from_seconds(divided_seconds)
        if isinstance(other, TimeDelta):
            total_seconds = self._timedelta.total_seconds()
            divided_seconds = other._timedelta.total_seconds()
            return int(total_seconds // divided_seconds)
        else:
            raise TypeError(
                "Unsupported operand type(s) for //: 'TimeDelta' and '{}'".format(
                    type(other)))

    def __lt__(self, other):
        if isinstance(other, TimeDelta):
            return self._timedelta < other._timedelta
        else:
            raise TypeError(
                "Unsupported operand type(s) for <: 'TimeDelta' and '{}'".format(
                    type(other)))

    def __gt__(self, other):
        if isinstance(other, TimeDelta):
            return self._timedelta > other._timedelta
        else:
            raise TypeError(
                "Unsupported operand type(s) for >: 'TimeDelta' and '{}'".format(
                    type(other)))

    def __eq__(self, other):
        if isinstance(other, TimeDelta):
            return self._timedelta == other._timedelta
        else:
            raise TypeError(
                "Unsupported operand type(s) for ==: 'TimeDelta' and '{}'".format(
                    type(other)))

    def __ge__(self, other):
        if isinstance(other, TimeDelta):
            return self._timedelta >= other._timedelta
        else:
            raise TypeError(
                "Unsupported operand type(s) for >=: 'TimeDelta' and '{}'".format(
                    type(other)))

    def __le__(self, other):
        if isinstance(other, TimeDelta):
            return self._timedelta <= other._timedelta
        else:
            raise TypeError(
                "Unsupported operand type(s) for <=: 'TimeDelta' and '{}'".format(
                    type(other)))

    def __abs__(self):
        return TimeDelta.from_timedelta(abs(self._timedelta))

    @property
    def years(self):
        return self._timedelta.days // 365

    @property
    def months(self):
        return (self._timedelta.days % 365) // 30

    @property
    def days(self):
        return self._timedelta.days % 30

    @property
    def hours(self):
        return self._timedelta.seconds // 3600

    @property
    def minutes(self):
        return (self._timedelta.seconds % 3600) // 60

    @property
    def seconds(self):
        return self._timedelta.seconds % 60

    @property
    def microseconds(self):
        return self._timedelta.microseconds

    @property
    def total_seconds(self):
        return self._timedelta.total_seconds()

    @classmethod
    def from_timedelta(cls, td):
        return cls(microsecond=td.microseconds, second=td.seconds % 60,
                   minute=(td.seconds // 60) % 60, hour=td.seconds // 3600,
                   day=td.days)

    @classmethod
    def from_seconds(cls, seconds):
        days, remaining_seconds = divmod(seconds, 86400)
        hours, remaining_seconds = divmod(remaining_seconds, 3600)
        minutes, seconds = divmod(remaining_seconds, 60)
        return cls(day=days, hour=hours, minute=minutes, second=seconds)
