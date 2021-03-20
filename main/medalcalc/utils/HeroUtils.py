import re
import random
from configparser import ConfigParser
from datetime import date
from typing import List

from MainSettings import MainSettings
from common.utils.DateUtils import DateUtils
from medalcalc.models.Element import Element
from medalcalc.models.Hero import Hero, Rarity
from medalcalc.utils.RaidEventUtils import RaidEventUtils, RaidBoss


class HeroUtils:

    MEDALS_NEEDED = {
        0: 0,
        1: 10,
        2: 30,
        3: 80,
        4: 280,
        5: 880,
        6: 2380,
        7: 4880
    }

    heroes: dict = {
        Element.WATER: {},
        Element.FIRE: {},
        Element.EARTH: {},
        Element.LIGHT: {},
        Element.DARK: {}
    }

    request: List[str]
    requestSunday: List[str]
    crusadeHeroes: List[str]

    magicMedals: float
    magicMedalHero: List[str]
    magicMedalsDaily: float

    guildShopCost = {
        Rarity.COMMON: 0,
        Rarity.RARE: 0,
        Rarity.EPIC: 0
    }
    guildShopFocus: dict = {}

    raidUtils: RaidEventUtils

    crusadeCoins: int = 0
    crusadeCoinsPerCrusade: int
    CRUSADE_MEDALS: int = 10
    CRUSADE_COST: int = 250

    def __init__(self):
        self.raidUtils = RaidEventUtils()

        config = MainSettings.config
        self.__initHeroes(config)

        settings = config["settings"]
        self.request = self.__splitNames(settings["request"])
        self.magicMedals = config.getfloat("settings", "mm")
        self.magicMedalHero = self.__splitNames(config.get("settings", "mmHero"))
        self.magicMedalsDaily = config.getfloat("settings", "mmDaily")
        self.requestSunday = self.__splitNames(config.get("settings", "requestSunday"))
        self.crusadeHeroes = self.__splitNames(config.get("settings", "crusadeHero"))
        self.crusadeCoinsPerCrusade = config.getfloat("settings", "crusadeCoins")

        self.guildShopCost[Rarity.COMMON] = config.getint("settings", "gcCommon")
        self.guildShopCost[Rarity.RARE] = config.getint("settings", "gcRare")
        self.guildShopCost[Rarity.EPIC] = config.getint("settings", "gcEpic")
        gcFocus = config.get("settings", "gcFocus").split("=")
        if len(gcFocus) == 2:
            self.guildShopFocus[0] = gcFocus[0]
            self.guildShopFocus[1] = int(gcFocus[1])

    def __initHeroes(self, config: ConfigParser):
        for element in Element:
            for rarity in Rarity:
                section = f"{element.value}.{rarity.value}"
                if section in config.sections():
                    heroes = config.items(section)
                    for hero in heroes:
                        self.__initHero(hero[0], hero[1], element, rarity)

    def __initHero(self, name: str, values: str, element: Element, rarity: Rarity):
        splitter = re.compile(' +')
        values = re.split(splitter, values)
        stars = int(values[0])
        medals = int(values[1])
        if stars >= 7:
            return

        extraMedals = False
        if len(values) > 2:
            flags = values[2]
            extraMedals = self.__getExtraMedalsFromFlags(flags)

        hero = Hero(name=name, stars=stars, medals=medals, element=element, rarity=rarity, extraMedals=extraMedals)
        self.heroes[element][name] = hero

    def __getExtraMedalsFromFlags(self, flags: str) -> bool:
        return "m" in flags

    def __splitNames(self, values: str) -> List[str]:
        result = []
        for value in values.split(","):
            result.append(value.strip())
        return result

    def getAllHeroes(self) -> List[Hero]:
        result = []
        for elementHeroes in self.heroes.values():
            for hero in elementHeroes.values():
                result.append(hero)

        return result

    def getHero(self, name: str) -> Hero:
        heroes = self.getAllHeroes()
        for hero in heroes:
            if hero.name == name:
                return hero

    def getUnmaxedHeroes(self, element: Element) -> dict:
        result = {}
        for elementHeroes in self.heroes.values():
            for hero in elementHeroes.values():
                if hero.element == element and not hero.isMaxed():
                    result[hero.name] = hero

        return result

    def getRarityHeroes(self, rarity: Rarity) -> List[Hero]:
        result = []
        for elementHeroes in self.heroes.values():
            for hero in elementHeroes.values():
                if hero.rarity == rarity:
                    result.append(hero)

        return result

    def getRequestHero(self) -> str:
        return self.request[0] if self.request else None

    def getRequestSundayHero(self) -> str:
        return self.requestSunday[0] if self.requestSunday else None

    def getMmHero(self) -> str:
        return self.magicMedalHero[0] if self.magicMedalHero else None

    def getCrusadeHero(self) -> str:
        return self.crusadeHeroes[0] if self.crusadeHeroes else None

    def removeRequestHero(self, hero: Hero):
        try:
            self.request.remove(hero.name)
        except ValueError:
            pass
        try:
            self.requestSunday.remove(hero.name)
        except ValueError:
            pass
        try:
            self.magicMedalHero.remove(hero.name)
        except ValueError:
            pass
        try:
            self.crusadeHeroes.remove(hero.name)
        except ValueError:
            pass

    def checkMax(self, result: List[Hero], heroes: dict, dungeonUtils):
        for hero in heroes.copy().values():
            if hero.isMaxed():
                result.append(hero)
                del heroes[hero.name]
                self.removeRequestHero(hero)
                dungeonUtils.checkEventTriggers(hero)

    def requestHero(self, heroes: dict, day: date):
        isSunday = day.isoweekday() == 7
        requestHero = self.getRequestHero()
        requestHeroSunday = self.getRequestSundayHero()

        for hero in heroes.values():
            if hero.name == requestHero or hero.name == requestHeroSunday:
                hero.incrementRequest(isSunday)

    def incrementMagicMedal(self):
        self.magicMedals += self.magicMedalsDaily

    def useMagicMedals(self, heroes: dict):
        if not self.magicMedals.is_integer():
            return

        mmHero = self.getMmHero()
        for hero in heroes.values():
            if hero.name == mmHero and hero.stars == 6:
                mmLeft = hero.incrementMagicMedals(int(self.magicMedals))
                self.magicMedals = max(0.0, mmLeft)

    def guildShop(self):
        for rarity in self.guildShopCost.keys():
            heroes = self.getRarityHeroes(rarity)
            if heroes:
                hero = random.choice(heroes)
                cost = self.guildShopCost.get(rarity)
                if self.guildShopFocus and hero.name == self.guildShopFocus[0]:
                    cost = self.guildShopFocus[1]

                hero.incrementGuildCoin(cost)

    def crusade(self):
        if DateUtils.days % 2 == 0:
            self.crusadeCoins += self.crusadeCoinsPerCrusade
            if self.crusadeCoins >= self.CRUSADE_COST:
                buys: int = int(self.crusadeCoins / self.CRUSADE_COST)
                medals: int = buys * self.CRUSADE_MEDALS
                hero: Hero = self.getHero(self.getCrusadeHero())
                if hero:
                    self.crusadeCoins -= buys * self.CRUSADE_COST
                    hero.increment(medals)

    def crusherChest(self):
        self.raidUtils.crusherChest(self.getAllHeroes())

    def allMaxed(self):
        for key in self.heroes:
            heroes = self.heroes[key]
            if len(heroes) > 0:
                return False
        return True
