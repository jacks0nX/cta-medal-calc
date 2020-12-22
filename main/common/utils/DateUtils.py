from datetime import date, timedelta

class DateUtils:

    DAY_NAMES = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]

    startDate: date
    currentDate: date
    days: int

    @staticmethod
    def init(day: date):
        DateUtils.days = 0
        DateUtils.startDate = day
        DateUtils.currentDate = day

    @staticmethod
    def nextDay():
        DateUtils.currentDate += timedelta(days=1)
        DateUtils.days += 1

    @staticmethod
    def isSunday() -> bool:
        return DateUtils.currentDate.isoweekday() == 7

    @staticmethod
    def isSaturday() -> bool:
        return DateUtils.currentDate.isoweekday() == 6

    @staticmethod
    def isMonday() -> bool:
        return DateUtils.currentDate.isoweekday() == 1

    @staticmethod
    def isTuesday() -> bool:
        return DateUtils.currentDate.isoweekday() == 2

    @staticmethod
    def isWednesday() -> bool:
        return DateUtils.currentDate.isoweekday() == 3

    @staticmethod
    def weekday() -> int:
        return DateUtils.currentDate.isoweekday()

    @staticmethod
    def dayname() -> str:
        return DateUtils.DAY_NAMES[DateUtils.currentDate.weekday()]

    @staticmethod
    def isGwRewardDay() -> bool:
        return DateUtils.currentDate.isoweekday() == 6

    @staticmethod
    def getDays() -> int:
        difference = DateUtils.currentDate - DateUtils.startDate
        return difference.days
