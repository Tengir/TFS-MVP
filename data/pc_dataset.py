from dataset import Dataset
from date_time.date_time import DateTime, TimeDelta
from utils.custom_enumerate import custom_enumerate


class PCDataset:
    """
    Конвертирует объект Dataset в таблицу значений, где столбцы это знач-ия
    одной метрики.
    Если начало метрики позже чем start_datetime, то все значения поедут,
    поэтому лучше указывать время чуть позже времени старта всех метрик.
    """

    def __init__(self, dataset: Dataset, start_datetime: DateTime,
                 finish_datetime: DateTime):
        count_metrics = dataset.get_count_metrics()
        step_timedelta = TimeDelta(0, 0, 1)
        self.keys = [""] * count_metrics  # value_name + tags - уникальные ключи метрик.
        self.table = [[0] * count_metrics for _ in range(
            (finish_datetime - start_datetime) // step_timedelta)]
        number_metric = 0  # Номер столбца которого заполняем в self.keys, self.table.

        repeat_values_metrics = {
            'PT1M': 60 // int(step_timedelta.total_seconds) - 1,
            'PT5M': 4 * 60 // int(step_timedelta.total_seconds) - 1,
            'PT24H': 24 * 60 * 60 // int(step_timedelta.total_seconds) - 1,
            'PT1H': 60 * 60 // int(step_timedelta.total_seconds) - 1}
        all_granularity = repeat_values_metrics.keys()
        for group_metric in dataset.group_metrics:
            # Для алгоритма PC нужно, чтобы были значения метрик на каждый
            # момент времени, но в данных некоторые метрики раз в 24 часа,
            # а другие раз в минуту. (Также есть раз в 5 минут и раз в 1 час).
            # Поэтому мы дополняем данные предыдущими значениями.
            # repeat_values_metrics - то сколько раз надо продублировать
            # значение.
            # step_timedelta - рассматриваемый промежуток времени. На наших
            # данных это 1 минута, меньше смысла нет.
            granularity = group_metric.granularity
            if granularity not in all_granularity:
                raise Exception("Нет функционала для подобной granularity")
            for metric in group_metric.metrics:
                # Перебираем время, чтобы найти время от start_datetime.
                start_index = 0
                for index, datetime in enumerate(metric.index):
                    if datetime >= start_datetime:
                        start_index = index
                        break
                self.keys[number_metric] = metric.value_name + "-" + "-".join(
                    metric.tags)

                # Начинаем заполнять таблицу
                repeat_values_metric = repeat_values_metrics[granularity]
                index_frame = 0
                for i, value in custom_enumerate(metric.values, start_index):
                    self.table[index_frame][number_metric] = value
                    index_frame += 1
                    for _ in range(repeat_values_metric):
                        self.table[index_frame][number_metric] = value
                        index_frame += 1

                # Если finish_datetime больше и нам не хватило значений, то
                # заполним оставшиеся ячейки последним заполненным значением.
                missing_values = self.table[index_frame - 1][number_metric]
                for i in range(index_frame, len(self.table)):
                    self.table[index_frame][number_metric] = missing_values

                number_metric += 1
