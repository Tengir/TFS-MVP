from data.dataset import Dataset
from date_time.date_time import TimeDelta

"""
То сколько значений метрик пропущено.
"""

ds = Dataset(r"C:\Users\Tengir\Desktop\tfs_20")

granularities = {
    'PT1M': TimeDelta(0, 0, 1),
    'PT5M':  TimeDelta(0, 0, 5),
    'PT24H':  TimeDelta(1, 0, 0),
    'PT1H':  TimeDelta(0, 1, 0)}

count_skip = 0
all_need_count = 0
all_have_count = 0
for gms in ds.group_metrics:
    granularity = gms.granularity
    for m in gms.metrics:
        start_index = m.index[0]
        finish_index = m.index[-1]
        need_count_values = (finish_index - start_index) // granularities[granularity]
        have_count_values = len(m.index)
        count_skip += need_count_values - have_count_values
        all_have_count += have_count_values
        all_need_count += need_count_values
print(all_need_count) # сколько должно было быть значений.
print(all_have_count) # сколько есть.
print(count_skip) # сколько скпинуто
print(count_skip / all_need_count)


"""
11195162
2188927
9006235
0.8044756297407756
"""

