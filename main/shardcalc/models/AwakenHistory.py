from datetime import date


class AwakenHistory:

    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    # YELLOW = '\033[93m'
    YELLOW = ''
    RED = '\033[91m'
    # BOLD = '\033[1m'
    BOLD = ''
    UNDERLINE = '\033[4m'
    # END = '\033[0m'
    END = ''

    NAME_LENGTH = 16
    STAR_LENGTH = 4
    DAY_LENGTH = 10
    DAYS_LENGTH = 6
    FOOTER_LENGTH = 46

    name: str
    awaken: int
    day: date
    days: int

    def __init__(self, name: str, day: date, days: int, awaken=7):
        self.name = name
        self.awaken = awaken
        self.day = day
        self.days = days

    def print(self):
        name = self.name.ljust(self.NAME_LENGTH).title()
        awaken = str(self.awaken).center(self.STAR_LENGTH)
        day = str(self.day).ljust(self.DAY_LENGTH)
        days = str(self.days).rjust(self.DAYS_LENGTH)

        start = ""
        end = ""

        print(start + f"{awaken} {name} {day} {days}" + end)

    @staticmethod
    def printHeader(element: str):
        name = "HERO".ljust(AwakenHistory.NAME_LENGTH)
        star = "STAR".ljust(AwakenHistory.STAR_LENGTH)
        day = "DATE".ljust(AwakenHistory.DAY_LENGTH)
        days = "DAYS".rjust(AwakenHistory.DAYS_LENGTH)
        print(AwakenHistory.BOLD + element.upper() + AwakenHistory.END)
        print(AwakenHistory.BOLD + f"{star} {name} {day} {days}" + AwakenHistory.END)

    @staticmethod
    def printFooter():
        print("".center(AwakenHistory.FOOTER_LENGTH, "-"))
