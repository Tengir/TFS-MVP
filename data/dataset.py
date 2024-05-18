import json
import os

from .group_metrics import GroupMetrics
from .metric import Metric


class Dataset:
    def __init__(self, folder_path: [str, None] = None):
        self.group_metrics = []
        if folder_path is not None:
            self.__read_from_json(folder_path)

    def __read_from_json(self, folder_path: str):
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, 'r') as file:
                    data = json.load(file)

                id_metrics: str = data.get('id_metrics')
                granularity: str = data.get('granularity')
                score: int = data.get('score')
                spike_drop = data.get('spike-drop')
                anomaly_minimum_duration: str = data.get(
                    'anomaly_minimum_duration')
                pipeline_id = data.get('pipeline_id')
                abs_delta_perc_delta = data.get(
                    'abs_delta-perc_delta')

                metrics = []
                for metric_data in data.get('metric_dataset', []):
                    values = metric_data.get('values', [])
                    index = metric_data.get('index', [])
                    orange_pos = metric_data.get('orange_pos', [])
                    grey_pos = metric_data.get('grey_pos', [])
                    lower = metric_data.get('lower', [])
                    upper = metric_data.get('upper', [])
                    value_name = metric_data.get('value_name')
                    tags = metric_data.get('tags', [])

                    metric = Metric(values, index, orange_pos, grey_pos, lower,
                                    upper, value_name, tags)
                    metrics.append(metric)

                group_metrics = GroupMetrics(id_metrics, granularity, score,
                                             spike_drop,
                                             anomaly_minimum_duration,
                                             pipeline_id, abs_delta_perc_delta,
                                             metrics)
                self.group_metrics.append(group_metrics)

    def get_count_metrics(self):
        ans = 0
        for gm in self.group_metrics:
            ans += len(gm.metrics)
        return ans
