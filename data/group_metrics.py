class GroupMetrics:
    def __init__(self, id_metrics, granularity, score, spike_drop, anomaly_minimum_duration, pipeline_id, abs_delta_perc_delta, metrics):
        self.id_metrics = id_metrics
        self.granularity = granularity
        self.score = score
        self.spike_drop = spike_drop
        self.anomaly_minimum_duration = anomaly_minimum_duration
        self.pipeline_id = pipeline_id
        self.abs_delta_perc_delta = abs_delta_perc_delta
        self.metrics = metrics