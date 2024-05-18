from data.dataset import Dataset
from date_time.date_time import DateTime


def get_max_min_datetime(ds: Dataset):
    max = DateTime(1, 1, 1)
    min = DateTime(9999, 1, 1)
    for gm in ds.group_metrics:
        for m in gm.metrics:
            if m.index[-1] > max:
                max = m.index[-1]
            if m.index[0] < min:
                min = m.index[0]
    return (min, max)
