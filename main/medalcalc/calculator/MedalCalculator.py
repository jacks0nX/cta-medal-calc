import json
import random
import re
from datetime import date
from operator import attrgetter
from typing import List, Optional

from MainSettings import MainSettings
from medalcalc.models.Hero import Hero
from medalcalc.models.HeroHistory import HeroHistory
from common.utils.DateUtils import DateUtils
from medalcalc.models.MedalType import MedalType
from medalcalc.utils.DungeonUtils import DungeonUtils
from medalcalc.utils.HeroUtils import HeroUtils, Element


class MedalCalculator:

    TIMEOUT_DAYS: int = 5000

    heroUtils: HeroUtils
    dungeonUtils = DungeonUtils

    heroes: dict
    elementX2: Element
    dailyTickets: int
    rebuys: int

    showHistory: bool
    heroFilter: List[str] = []
    calcElements: List[str] = []

    result: List[Hero] = []

    def __init__(self):
        HeroUtils()
        self.dungeonUtils = DungeonUtils()
        self.heroUtils = HeroUtils()

        # settings
        self.showHistory = MainSettings.config.getboolean("calculator", "showHistory")
        self.showHistory = MainSettings.config.getboolean("calculator", "showHistory")
        for value in MainSettings.config.get("calculator", "heroFilter").split(","):
            if value != '':
                self.heroFilter.append(value.strip())
        farmElements = re.split(' +', MainSettings.config.get("calculator", "elements"))
        for element in farmElements:
            self.calcElements.append(element)

    def calculateMedals(self):
        # dates
        DateUtils.init(date.today())

        # dungeons
        self.dailyTickets = self.dungeonUtils.ticketsDaily

        # x2
        extraTicketsConfig = self.dungeonUtils.ticketsExtraX2
        extraTickets = extraTicketsConfig
        self.rebuys = self.dungeonUtils.rebuysX2

        # initially skip the current day
        DateUtils.nextDay()

        while True:
            isX2 = self.dungeonUtils.isDoubleDungeon(DateUtils.currentDate)
            element = self.dungeonUtils.elementX2 if isX2 else self.dungeonUtils.getDungeon()
            if element:
                extraTickets = extraTickets if isX2 else 0
                self.heroes = self.heroUtils.heroes[element]

                if len(self.heroes) > 0:
                    self.simulateTickets(
                        isX2=isX2,
                        extraTickets=extraTickets
                    )
                    if not isX2:
                        extraTickets = extraTicketsConfig
            ##################

            # cc
            self.heroUtils.crusherChest()
            self.heroUtils.checkMax(self.result, self.heroes, self.dungeonUtils)

            # guild shop
            self.heroUtils.guildShop()
            self.heroUtils.checkMax(self.result, self.heroes, self.dungeonUtils)

            self.heroUtils.crusade()
            self.heroUtils.checkMax(self.result, self.heroes, self.dungeonUtils)

            # request
            self.heroUtils.requestHero(self.heroes, DateUtils.currentDate)
            self.heroUtils.checkMax(self.result, self.heroes, self.dungeonUtils)

            # mm
            self.heroUtils.incrementMagicMedal()
            self.heroUtils.useMagicMedals(self.heroes)
            self.heroUtils.checkMax(self.result, self.heroes, self.dungeonUtils)

            # check finished
            if self.isFinished():
                return
            ###########

            # next day
            DateUtils.nextDay()

            # timeout
            if DateUtils.days > self.TIMEOUT_DAYS:
                raise Exception(f"Timeout after {self.TIMEOUT_DAYS} days: {DateUtils.days}")
            ###############
            #########################

    def simulateTickets(
            self,
            isX2: bool = False,
            extraTickets: int = 0):
        totalTickets = self.dailyTickets + extraTickets
        medalType = MedalType.DUNGEON
        if isX2:
            totalTickets += (self.rebuys * 10)
            medalType = MedalType.DUNGEON_X2

        medalIncrement = 2 if isX2 else 1

        for ticket in range(totalTickets):
            if not self.heroes:
                return

            # draw hero
            hero = self.randomHero(self.heroes)
            if hero:
                hero.increment(medalIncrement, type=medalType)
                self.heroUtils.checkMax(self.result, self.heroes, self.dungeonUtils)

            # draw common
            commonHero = self.randomHero(self.heroes, common=True)
            if commonHero:
                commonHero.increment(medalIncrement, type=medalType)
                if commonHero is not hero:
                    self.heroUtils.checkMax(self.result, self.heroes, self.dungeonUtils)

    def randomHero(self, heroMap, common: bool = False) -> Optional[Hero]:
        heroes = list(heroMap)
        if common:
            commonFilter = filter(lambda commonHero: commonHero.isCommon(), heroMap.values())
            heroes = list(map(lambda commonHero: commonHero.name, commonFilter))

        if not heroes:
            return None

        heroName = random.choice(heroes)
        return heroMap[heroName]

    def isFinished(self) -> bool:
        for calcElement in self.calcElements:
            element = Element(calcElement)
            if self.heroUtils.heroes[element]:
                return False
        return True

    def print(self, sort: bool):
        for element in self.calcElements:
            self.__printElement(element=Element(element), sort=sort, showHistory=self.showHistory)

    def __printElement(self, element: Element, sort=False, showHistory=False):
        HeroHistory.printHeader(element.value)

        if sort:
            histories: List[HeroHistory] = []
            for hero in self.result:
                if hero.element == element and (not self.heroFilter or hero.name in self.heroFilter):
                    for hist in hero.history:
                        if showHistory or hist.isMax():
                            histories.append(hist)

            histories = sorted(histories, key=attrgetter('days'))

            for hist in histories:
                hist.print()

        if not sort:
            for hero in self.result:
                hero.print(history=showHistory)

        HeroHistory.printFooter()

    def printSettings(self):
        print(f"Settings")
        HeroHistory.printFooter()
        length = 25
        print(f"Request (common):".ljust(length) + str(self.heroUtils.request))
        print(f"Request (sunday):".ljust(length) + str(self.heroUtils.requestSunday))
        print(f"MM Hero:".ljust(length) + str(self.heroUtils.magicMedalHero))
        print(f"Element x2:".ljust(length) + self.dungeonUtils.elementX2.value)
        print(f"Dungeon daily tickets:".ljust(length) + str(self.dungeonUtils.ticketsDaily))
        print(f"Dungeon x2 extra tickets:".ljust(length) + str(self.dungeonUtils.ticketsExtraX2))
        print(f"Dungeon x2 rebuys:".ljust(length) + str(self.dungeonUtils.rebuysX2))
        print(f"Weekly dungeons:".ljust(length) + json.dumps(self.dungeonUtils.dailyDungeons))
