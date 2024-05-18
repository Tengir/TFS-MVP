from data.dataset import Dataset
from date_time.date_time import DateTime, TimeDelta
from utils.custom_enumerate import custom_enumerate
from data.metric import Metric


class PCDatasetExample:
    """
    Класс для показа на малом кол-ве данных.
    Конвертирует объект Dataset в таблицу значений, где столбцы это знач-ия
    одной метрики.
    Берет только метрики 5 минутной гранулярности.
    """

    def __init__(self, dataset: Dataset, start_datetime: DateTime,
                 finish_datetime: DateTime):
        # Список со списком всех дат, которые будут.
        all_datetime = self.__date_range(start_datetime, finish_datetime)

        # Берем группы только с 5 минутным сбора.
        group_metrics = []
        for group_metric in dataset.group_metrics:
            if group_metric.granularity == "PT5M":
                group_metrics.append(group_metric)

                delete_metric = set()
                # Удалим метрики, кот-ые не подходят из-за данных.
                for index, metric in enumerate(group_metric.metrics):
                    if not self.__is_ok_metric(metric, start_datetime,
                                               finish_datetime):
                        delete_metric.add(index)

                group_metric.metrics = [group_metric.metrics[i] for i in
                                        set(range(
                                            len(group_metric.metrics))) - delete_metric]

        new_dataset = Dataset()
        new_dataset.group_metrics = group_metrics

        count_metrics = new_dataset.get_count_metrics()
        step_timedelta = TimeDelta(0, 0, 5)
        self.keys = [
                        ""] * count_metrics  # value_name + tags - уникальные ключи метрик.
        self.table = [["Х"] * count_metrics for _ in range(
            (finish_datetime - start_datetime) // step_timedelta + 1)]
        number_metric = 0  # Номер столбца которого заполняем в self.keys, self.table.

        for group_metric in new_dataset.group_metrics:
            for metric in group_metric.metrics:
                self.keys[number_metric] = metric.value_name + "-" + "-".join(
                    metric.tags)
                # Перебираем время, чтобы найти время от start_datetime.
                start_index = 0
                for index, datetime in enumerate(metric.index):
                    if datetime >= start_datetime:
                        start_index = index
                        break

                # Начинаем заполнять таблицу
                for i, value in custom_enumerate(metric.values, start_index):
                    if metric.index[start_index + i] > finish_datetime:
                        break
                    index_frame = all_datetime.index(self.__get_nearest_5min_datetime(metric.index[start_index + i]))
                    self.table[index_frame][number_metric] = value

                number_metric += 1

    def __is_ok_metric(self, metric: Metric, start_datetime: DateTime,
                       finish_datetime: DateTime) -> bool:
        # Удалим метрики, кот-ых нет на начало.
        if metric.index[0] - start_datetime > TimeDelta(0, 1):
            print("Начало")
            print(metric.index[0])
            print(start_datetime)
            print()
            return False
        # Удалим метрики, кот-ых не хватило до конца.
        if finish_datetime - metric.index[-1] > TimeDelta(0, 1):
            print("Конец")
            print(metric.index[-1])
            print(finish_datetime)
            print()
            return False

        # Удалим метрики с большими пропусками в данных > 60 минут.
        # Перебираем время, чтобы найти нужный промежуток.
        start_index = 0
        for index, datetime in enumerate(metric.index):
            if datetime >= start_datetime:
                start_index = index
                break
        finish_index = 0
        for index, datetime in enumerate(metric.index):
            if datetime > finish_datetime:
                finish_index = index
                break
        range_metric_indexes = [start_datetime] + metric.index[
                                                  start_index:finish_index] + [
                                   finish_datetime]
        for i in range(len(range_metric_indexes) - 1):
            if abs(range_metric_indexes[i] - range_metric_indexes[
                i + 1]) > TimeDelta(0, 1, 0):
                return False

        max_count_values = (finish_datetime - start_datetime) // TimeDelta(0,
                                                                           0,
                                                                           5)
        # Удалим метрики у которых слишком мало значений в этом промежутке.
        # оставим
        if (finish_index - start_index) / max_count_values < 0.5:
            return False
        # Удалим неинтересные метрики, у которых много значений 0.
        if metric.values.count(0.0) > max_count_values * 0.5:
            return False
        return True

    @staticmethod
    def __get_nearest_5min_datetime(dt: DateTime):
        minutes = dt.minute
        remaining_minutes = minutes % 5

        if remaining_minutes > 2:
            delta = TimeDelta(minute=5 - remaining_minutes)
        else:
            delta = TimeDelta(minute=-remaining_minutes)

        nearest_5min_dt = dt + delta
        return DateTime(nearest_5min_dt.year, nearest_5min_dt.month, nearest_5min_dt.day, nearest_5min_dt.hour, nearest_5min_dt.minute)

    @staticmethod
    def __date_range(start_date: DateTime, end_date: DateTime):
        current_date = start_date
        dates = []

        while current_date <= end_date:
            dates.append(current_date)
            current_date += TimeDelta(minute=5)

        return dates
