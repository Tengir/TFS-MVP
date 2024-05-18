import matplotlib.pyplot as plt
from data.dataset import Dataset
from date_time.date_time import DateTime
import matplotlib
from datetime import timedelta, datetime

"""
В этом файле я строил графики, количество метрик на каждую дату, но в более
крупном масштабе.
"""

def date_range(start_date, end_date):
    current_date = start_date
    dates = []

    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(minutes=5)

    return [date.strftime('%#d-%H-%M') for date in dates]


def get_nearest_5min_datetime(dt):
    minutes = dt.minute
    remaining_minutes = minutes % 5

    if remaining_minutes > 2:
        delta = timedelta(minutes=5 - remaining_minutes)
    else:
        delta = timedelta(minutes=-remaining_minutes)

    nearest_5min_dt = dt + delta
    return nearest_5min_dt


matplotlib.use('TkAgg')

ds = Dataset(r"C:\Users\Tengir\Desktop\tfs_20")

dates = dict()
start = datetime(2023, 6, 4)
end = datetime(2023, 6, 8)
dates_range = date_range(start, end)
print(dates_range)
for dict_ in [dates]:
    for date in dates_range:
        dict_[date] = 0

for gms in ds.group_metrics:
    if gms.granularity != "PT5M":
        continue
    for m in gms.metrics:
        for ind in m.index:
            if ind < DateTime.from_datetime(
                    start) or ind > DateTime.from_datetime(end):
                continue
            date = get_nearest_5min_datetime(ind._datetime)
            dates[date.strftime('%#d-%H-%M')] += 1

# Создаем списки дат и количеств для построения графика
unique_dates = list(dates.keys())
counts = list(dates.values())

# Создаем график
plt.figure(figsize=(10, 6))
plt.plot(unique_dates, counts)

# Устанавливаем подписи на оси x через каждые 10 элементов
plt.xticks(unique_dates[::20], unique_dates[::20], rotation=90)

plt.xlabel('Дата')
plt.ylabel('Количество')
plt.grid(True)
plt.show()