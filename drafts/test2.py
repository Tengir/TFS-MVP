import matplotlib.pyplot as plt
from data.dataset import Dataset
import matplotlib
from datetime import timedelta, datetime

"""
В этом файле я строил графики, количество метрик на каждую дату, чтобы
найти дату когда метрик больше всего.
"""

def date_range(start_date, end_date):
    """
    Функция для генерации списка дат между start_date и end_date (включительно).

    Аргументы:
    start_date (datetime.date): начальная дата
    end_date (datetime.date): конечная дата

    Возвращает:
    list: список дат между start_date и end_date (включительно)
    """
    delta = end_date - start_date
    dates = []
    for i in range(delta.days + 1):
        date = start_date + timedelta(days=i)
        dates.append(date)
    return [date.strftime('%Y-%#m-%#d') for date in dates]

matplotlib.use('TkAgg')

ds = Dataset(r"C:\Users\Tengir\Desktop\tfs_20")

dates = dict()
starts = dict()
ends = dict()
dates_range = date_range(datetime(2023,5,1), datetime(2023, 6, 10))
print(dates_range)
for dict_ in [dates, starts, ends]:
    for date in dates_range:
        dict_[date] = 0

for gms in ds.group_metrics:
    if gms.granularity != "PT5M":
        continue
    for m in gms.metrics:
        index = [f"{ind.year}-{ind.month}-{ind.day}" for ind in m.index]
        starts[f"{m.index[0].year}-{m.index[0].month}-{m.index[0].day}"] += 1
        ends[f"{m.index[-1].year}-{m.index[-1].month}-{m.index[-1].day}"] += 1
        for date in m.index:
            dates[f"{date.year}-{date.month}-{date.day}"] += 1


# Создаем списки дат и количеств для построения графика
unique_dates = list(dates.keys())
counts = list(dates.values())

# Создаем график
plt.figure(figsize=(10, 6))
plt.bar(unique_dates, counts, align='center')
plt.xlabel('Дата')
plt.ylabel('Количество')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()


# Создаем списки дат и количеств для построения графика
unique_dates = list(starts.keys())
counts = list(starts.values())

# Создаем график
plt.figure(figsize=(10, 6))
plt.bar(unique_dates, counts, align='center')
plt.xlabel('Дата')
plt.ylabel('Количество')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Создаем списки дат и количеств для построения графика
unique_dates = list(ends.keys())
counts = list(ends.values())

# Создаем график
plt.figure(figsize=(10, 6))
plt.bar(unique_dates, counts, align='center')
plt.xlabel('Дата')
plt.ylabel('Количество')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

