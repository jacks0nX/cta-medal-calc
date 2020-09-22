from datetime import date, timedelta

class DataStore:

    startDate: date
    currentDate: date
    days: int

    @staticmethod
    def init(day: date):
        DataStore.days = 0
        DataStore.startDate = day
        DataStore.currentDate = day

    @staticmethod
    def nextDay():
        DataStore.currentDate += timedelta(days=1)

    @staticmethod
    def isSunday() -> bool:
        return DataStore.currentDate.isoweekday() == 7

    @staticmethod
    def weekday() -> int:
        return DataStore.currentDate.isoweekday()

    @staticmethod
    def getDays() -> int:
        difference = DataStore.currentDate - DataStore.startDate
        return difference.days
