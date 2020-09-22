from enum import Enum

from models.HeroHistory import HeroHistory
from utils.DataStore import DataStore


class Rarity(Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"

    def isCommon(self):
        return self.value == self.COMMON.value


class Hero:

    __MEDALS_NEEDED = {
        0: 0,
        1: 10,
        2: 30,
        3: 80,
        4: 280,
        5: 880,
        6: 2380,
        7: 4880
    }

    history: [HeroHistory] = []

    name: str
    stars: int
    medals: int
    rarity: Rarity
    mmUsed: int = 0
    extraMedals: bool

    def __init__(self, name, stars, medals, rarity=Rarity.RARE, extraMedals=False):
        self.name = name
        self.stars = stars
        self.medals = medals
        self.rarity = rarity
        self.history = []
        self.extraMedals = extraMedals

    def increment(self, medalIncrement: int = 1, extraMedals=False):
        originalStars = self.stars
        nextMedals = self.medals + medalIncrement
        needed = self.__MEDALS_NEEDED
        total = needed[self.stars] + nextMedals
        resultStars = 0

        for star in range(7, 0, -1):
            if total >= needed[star]:
                resultStars = star
                break

        resultMedals = 0
        if resultStars < 7:
            resultMedals = total - needed[resultStars]

        self.stars = resultStars
        self.medals = resultMedals

        hasEvolved = originalStars < resultStars
        if hasEvolved:
            self.__addHistory(resultStars)

        if originalStars < 6 and resultStars == 6 and self.extraMedals and not extraMedals:
            self.increment(400, extraMedals=True)

    def incrementRequest(self, isSunday: bool):
        if self.isCommon():
            medals = 0 if isSunday else 30
        else:
            medals = 10 if isSunday else 0

        self.increment(medals)

    def __addHistory(self, star: int):
        day = DataStore.currentDate
        days = DataStore.getDays()
        if days == 0:
            return
        historyEntry = HeroHistory(self.name,  day, days, star, mm=self.mmUsed)
        self.history.insert(0, historyEntry)

    def isMaxed(self):
        return self.stars >= 7

    def isCommon(self):
        return self.rarity.isCommon()

    def print(self, history: bool = False):
        histories = self.history
        if not history:
            histories = list(filter(lambda hist: hist.isMax(), histories))

        for history in histories:
            history.print()

    def incrementMagicMedals(self, magicMedals: int):
        medalsFromMm = 4
        if self.isCommon():
            medalsFromMm = 30
        elif self.rarity == Rarity.RARE:
            medalsFromMm = 10

        self.mmUsed += int(magicMedals)
        medals = int(magicMedals) * medalsFromMm
        self.increment(medals)
