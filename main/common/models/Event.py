import datetime


class Event:

    content = None
    start: datetime.date
    end: datetime.date

    def __init__(self, start: datetime.date, end: datetime.date):
        self.start = start
        self.end = end

    def isBetween(self, day: datetime.date) -> bool:
        return self.start <= day <= self.end
