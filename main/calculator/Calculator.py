import random
from datetime import date
from operator import attrgetter
from typing import List

from models.Hero import Hero
from models.HeroHistory import HeroHistory
from utils.DataStore import DataStore
from utils.DungeonUtils import DungeonUtils
from utils.HeroUtils import Element, HeroUtils


class Calculator:

    TIMEOUT_DAYS: int = 5000

    heroUtils: HeroUtils

    def calculateMedals(self, element: Element, elementX2: Element = None) -> List[Hero]:
        dungeonUtils = DungeonUtils()
        self.heroUtils = HeroUtils()

        elementX2 = elementX2 if elementX2 else dungeonUtils.elementX2

        # dates
        DataStore.init(date.today())

        # heroes
        heroes = self.heroUtils.heroes[element.value]
        result: List[Hero] = []

        # dungeons
        dailyTickets = dungeonUtils.ticketsDaily
        weeklyDungeons = dungeonUtils.weeklyDungeons[element.value]
        farmedDays = dungeonUtils.getFarmedDays(DataStore.currentDate, element)
        if weeklyDungeons == 0:
            return []

        # x2
        extraTicketsConfig = dungeonUtils.ticketsExtraX2
        extraTickets = extraTicketsConfig
        rebuysX2 = dungeonUtils.rebuysX2

        while True:
            isDungeonX2 = dungeonUtils.isDoubleDungeonDay(DataStore.currentDate, element, elementX2)

            if isDungeonX2:
                self.simulateTickets(
                    heroes=heroes,
                    dailyTickets=dailyTickets,
                    result=result,
                    x2=True,
                    extraTickets=extraTickets,
                    rebuysX2=rebuysX2
                )
            ###############

            # reset extra tickets
            if not isDungeonX2:
                extraTickets = extraTicketsConfig

            # simulate tickets
            isCorrectDungeon = dungeonUtils.isDungeonDay(DataStore.weekday(), element)
            if not isDungeonX2 and isCorrectDungeon and farmedDays < weeklyDungeons:
                farmedDays += 1
                self.simulateTickets(
                    heroes=heroes,
                    dailyTickets=dailyTickets,
                    result=result
                )
            ##############

            # request
            self.heroUtils.requestHero(heroes, DataStore.currentDate)

            # mm
            self.heroUtils.incrementMagicMedal()
            self.heroUtils.useMagicMedals(heroes)

            # check finished
            allMaxed = len(heroes) <= 0
            if allMaxed:
                return result
            ###########

            # next day
            DataStore.nextDay()

            # timeout
            if DataStore.days > self.TIMEOUT_DAYS:
                raise Exception(f"Timeout after {self.TIMEOUT_DAYS} days: {DataStore.days}")
            ###############

            # reset week
            if DataStore.weekday() == 1:
                farmedDays = 0
            #########################

    def simulateTickets(
            self,
            heroes: dict,
            dailyTickets: int,
            result: list,
            x2: bool = False,
            extraTickets: int = 0,
            rebuysX2: int = 0):
        totalTickets = dailyTickets + extraTickets + rebuysX2
        medalIncrement = 2 if x2 else 1

        for ticket in range(totalTickets):
            if len(heroes) == 0:
                return

            hero = self.randomHero(heroes)
            hero.increment(medalIncrement)

            if hero.isMaxed():
                result.append(hero)
                del heroes[hero.name]
                self.heroUtils.removeRequestHero(hero)
                continue

            if hero.isCommon():
                commonHero = self.randomHero(heroes, common=True)
                commonHero.increment(medalIncrement * 2)
                if commonHero.isMaxed():
                    result.append(commonHero)
                    del heroes[commonHero.name]
                    self.heroUtils.removeRequestHero(hero)

    def randomHero(self, heroMap, common: bool = False) -> Hero:
        heroes = list(heroMap)
        if common:
            commonFilter = filter(lambda commonHero: commonHero.isCommon(), heroMap.values())
            heroes = list(map(lambda commonHero: commonHero.name, commonFilter))

        heroName = random.choice(heroes)
        return heroMap[heroName]

    def print(self, results: List[Hero], element: Element, sort=False, showHistory=False):
        HeroHistory.printHeader(element.value)

        if sort:
            histories: List[HeroHistory] = []
            for hero in results:
                for hist in hero.history:
                    if showHistory or hist.isMax():
                        histories.append(hist)

            histories = sorted(histories, key=attrgetter('days'))
            for hist in histories:
                hist.print()

        if not sort:
            for hero in results:
                hero.print(history=showHistory)

        HeroHistory.printFooter()
