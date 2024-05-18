from date_time.date_time import DateTime

class Metric:
    def __init__(self, values, index, orange_pos, grey_pos, lower, upper, value_name, tags):
        self.values = values
        self.index = [DateTime(datetime) for datetime in index]
        self.orange_pos = orange_pos
        self.grey_pos = grey_pos
        self.lower = lower
        self.upper = upper
        self.value_name = value_name
        self.tags = tags