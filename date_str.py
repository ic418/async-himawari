import datetime

class HourlyIterator:
    def __init__(self, start_date, end_date):
        self.current_date = start_date
        self.end_date = end_date

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_date > self.end_date:
            raise StopIteration
        current = self.current_date
        self.current_date += datetime.timedelta(hours=1)
        return current.strftime('%Y-%m-%d-%H')

# 使用迭代器
start_date = datetime.datetime(2024, 1, 1, 0)
end_date = datetime.datetime(2024, 1, 1, 1)

hourly_iterator = HourlyIterator(start_date, end_date)
if __name__ == "__main__":
    for hour in hourly_iterator:
        print(hour)