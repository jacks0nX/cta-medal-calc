from medalcalc.models.Element import Element
from medalcalc.models.HeroHistory import HeroHistory
from common.utils.DateUtils import DateUtils
from medalcalc.models.MedalType import MedalType
from medalcalc.models.Rarity import Rarity


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

    __MAGIC_MEDALS = {
        Rarity.COMMON: 30,
        Rarity.RARE: 10,
        Rarity.EPIC: 4
    }

    history: [HeroHistory] = []

    name: str
    stars: int
    medals: int
    rarity: Rarity
    mmUsed: int = 0
    extraMedals: bool
    element: Element

    medalTypes: dict = {
        MedalType.DEFAULT: 0,
        MedalType.DUNGEON: 0,
        MedalType.DUNGEON_X2: 0,
        MedalType.GUILD_SHOP: 0,
        MedalType.MM: 0,
        MedalType.REQUEST: 0,
        MedalType.CC: 0,
    }

    def __init__(self, name, stars, medals, element: Element, rarity=Rarity.RARE, extraMedals=False):
        self.name = name
        self.stars = stars
        self.medals = medals
        self.rarity = rarity
        self.history = []
        self.extraMedals = extraMedals
        self.element = element

    def increment(self, medalIncrement: int = 1, extraMedals=False, type: MedalType = MedalType.DEFAULT):
        originalStars = self.stars
        nextMedals = self.medals + medalIncrement
        needed = self.__MEDALS_NEEDED
        total = needed[self.stars] + nextMedals
        resultStars = 0

        for star in range(7, 0, -1):
            if total >= needed[star]:
                resultStars = star
                break

        self.medalTypes[type] += medalIncrement

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

        self.increment(medals, type=MedalType.REQUEST)

    def __addHistory(self, star: int):
        day = DateUtils.currentDate
        days = DateUtils.getDays()
        if days == 0:
            return
        historyEntry = HeroHistory(self.name,  day, days, star, mm=self.mmUsed)
        historyEntry.medalTypes = self.medalTypes.copy()
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
        if magicMedals == 0:
            return 0.0

        medalsFromMm = self.__MAGIC_MEDALS.get(self.rarity)

        self.mmUsed += 1
        magicMedals -= 1
        self.increment(medalsFromMm, type=MedalType.MM)
        if self.isMaxed():
            return float(magicMedals)
        return self.incrementMagicMedals(magicMedals)

    def incrementGuildCoin(self, guildCoins: int):
        medals = max(int(guildCoins / self.rarity.getGuildCoins()) - 1, 0)
        self.increment(medals, type=MedalType.GUILD_SHOP)
