from date_time.date_time import DateTime, TimeDelta

a, b = DateTime(2023, 6, 5), DateTime(2023, 6, 7)
c = b - a
print(c)
t = TimeDelta(0, 0, 5)
print(c // t)