import re
from collections import namedtuple
from datetime import date
from enum import Enum
from typing import List

from models.Hero import Hero, Rarity
from settings.SettingsUtils import SettingsUtils


class Element(Enum):
    WATER = "water"
    EARTH = "earth"
    FIRE = "fire"
    LIGHT = "light"
    DARK = "dark"


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

    heroes = {
        "water": {},
        "earth": {},
        "fire": {},
        "light": {},
        "dark": {}
    }

    request: List[str]
    requestSunday: List[str]

    magicMedals: float
    magicMedalHero: List[str]
    magicMedalsDaily: float

    def __init__(self):
        config = SettingsUtils.config
        self.__initHero(config["heroes.water"], Element.WATER)
        self.__initHero(config["heroes.earth"], Element.EARTH)
        self.__initHero(config["heroes.fire"], Element.FIRE)
        self.__initHero(config["heroes.light"], Element.LIGHT)
        self.__initHero(config["heroes.dark"], Element.DARK)

        settings = config["settings"]
        self.request = self.__splitNames(settings["request"])
        self.magicMedals = float(settings["mm"])
        self.magicMedalHero = self.__splitNames(settings["mmHero"])
        self.magicMedalsDaily = float(settings["mmDaily"])
        self.requestSunday = self.__splitNames(settings["requestSunday"])

    def __initHero(self, pool, element: Element):
        splitter = re.compile(' +')
        for key in pool:
            values = re.split(splitter, pool[key])
            stars = int(values[0])
            if stars >= 7:
                continue

            rarity = Rarity.EPIC
            extraMedals = False
            if len(values) > 2:
                flags = values[2]
                rarity = self.__getRarityFromFlags(flags)
                extraMedals = self.__getExtraMedalsFromFlags(flags)

            hero = Hero(name=key, stars=stars, medals=int(values[1]), rarity=rarity, extraMedals=extraMedals)
            self.heroes[element.value][hero.name] = hero

    def __getRarityFromFlags(self, flags: str) -> Rarity:
        if "e" in flags:
            return Rarity.EPIC
        if "c" in flags:
            return Rarity.COMMON
        return Rarity.RARE

    def __getExtraMedalsFromFlags(self, flags: str) -> bool:
        return "m" in flags

    def __splitNames(self, values: str) -> List[str]:
        result = []
        for value in values.split(","):
            result.append(value.strip())
        return result

    def getRequestHero(self) -> str:
        return self.request[0] if self.request else None

    def getRequestSundayHero(self) -> str:
        return self.requestSunday[0] if self.requestSunday else None

    def getMmHero(self) -> str:
        return self.magicMedalHero[0] if self.magicMedalHero else None

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
            if hero.name == mmHero:
                hero.incrementMagicMedals(self.magicMedals)
                self.magicMedals = 0
