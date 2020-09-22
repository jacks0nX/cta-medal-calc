from datetime import date


class HeroHistory:

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
    MM_LENGTH = 6
    FOOTER_LENGTH = 46

    name: str
    star: int
    day: date
    days: int
    mm: int

    def __init__(self, name: str, day: date, days: int, star=7, mm=0):
        self.name = name
        self.star = star
        self.day = day
        self.days = days
        self.mm = mm

    def isMax(self):
        return self.star == 7

    def print(self):
        name = self.name.ljust(self.NAME_LENGTH).title()
        star = str(self.star).center(self.STAR_LENGTH)
        day = str(self.day).ljust(self.DAY_LENGTH)
        days = str(self.days).rjust(self.DAYS_LENGTH)

        mm = ""
        if (self.mm > 0):
            mm = self.mm
        mm = str(mm).rjust(self.MM_LENGTH)

        start = ""
        end = ""
        if self.isMax():
            start = self.YELLOW
            end = self.END

        print(start + f"{star} {name} {day} {days} {mm}" + end)

    @staticmethod
    def printHeader(element: str):
        name = "HERO".ljust(HeroHistory.NAME_LENGTH)
        star = "STAR".ljust(HeroHistory.STAR_LENGTH)
        day = "DATE".ljust(HeroHistory.DAY_LENGTH)
        days = "DAYS".rjust(HeroHistory.DAYS_LENGTH)
        mm = "MM".rjust(HeroHistory.MM_LENGTH)
        print(HeroHistory.BOLD + element.upper() + HeroHistory.END)
        print(HeroHistory.BOLD + f"{star} {name} {day} {days} {mm}" + HeroHistory.END)

    @staticmethod
    def printFooter():
        print("".center(HeroHistory.FOOTER_LENGTH, "-"))
