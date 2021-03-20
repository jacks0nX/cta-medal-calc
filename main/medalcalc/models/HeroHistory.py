from datetime import date

from medalcalc.models.MedalType import MedalType


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

    medalTypes: dict = {
        MedalType.DEFAULT: 0,
        MedalType.DUNGEON: 0,
        MedalType.DUNGEON_X2: 0,
        MedalType.GUILD_SHOP: 0,
        MedalType.MM: 0,
        MedalType.REQUEST: 0,
        MedalType.CC: 0,
    }

    def __init__(self, name: str, day: date, days: int, star=7, mm=0, type: MedalType = MedalType.DEFAULT):
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
        if self.mm > 0:
            mm = self.mm
        mm = str(mm).rjust(self.MM_LENGTH)

        start = ""
        end = ""
        if self.isMax():
            start = self.YELLOW
            end = self.END


        blank = "".ljust(14)
        medalInfo = self.getMedalInfo()
        # print(start + f"{star} {name} {day} {days} {mm} {blank} {medalInfo}" + end)
        print(start + f"{star} {name} {day} {days} {mm}" + end)

    def getMedalInfo(self) -> str:
        dungeon = str(self.medalTypes[MedalType.DUNGEON]).rjust(4)
        dungeonX2 = str(self.medalTypes[MedalType.DUNGEON_X2]).rjust(4)
        gc = str(self.medalTypes[MedalType.GUILD_SHOP]).rjust(4)
        mm = str(self.medalTypes[MedalType.MM]).rjust(4)
        request = str(self.medalTypes[MedalType.REQUEST]).rjust(4)
        cc = str(self.medalTypes[MedalType.CC]).rjust(4)
        return f"{dungeon} {dungeonX2} {gc} {mm} {request} {cc}"

    @staticmethod
    def printHeader(element: str):
        name = "HERO".ljust(HeroHistory.NAME_LENGTH)
        star = "STAR".ljust(HeroHistory.STAR_LENGTH)
        day = "DATE".ljust(HeroHistory.DAY_LENGTH)
        days = "DAYS".rjust(HeroHistory.DAYS_LENGTH)
        mm = "MM".rjust(HeroHistory.MM_LENGTH)
        print(HeroHistory.BOLD + element.upper() + HeroHistory.END)

        blank = "".rjust(14)
        dungeon = "DNG".rjust(4)
        dungeonX2 = "X2".rjust(4)
        gc = "GC".rjust(4)
        mm2 = "MM".rjust(4)
        request = "REQ".rjust(4)
        cc = "CC".rjust(4)
        medalInfo = f"{dungeon} {dungeonX2} {gc} {mm2} {request} {cc}"

        # print(HeroHistory.BOLD + f"{star} {name} {day} {days} {mm} {blank} {medalInfo}" + HeroHistory.END)
        print(HeroHistory.BOLD + f"{star} {name} {day} {days} {mm}" + HeroHistory.END)

    @staticmethod
    def printFooter():
        print("".center(HeroHistory.FOOTER_LENGTH, "-"))
