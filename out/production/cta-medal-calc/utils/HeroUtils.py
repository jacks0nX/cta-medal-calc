import re
from collections import namedtuple
from datetime import date
from enum import Enum

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

    request: str
    requestSunday: str

    magicMedals: float
    magicMedalHero: int
    magicMedalsDaily: float

    def __init__(self):
        config = SettingsUtils.config
        self.__initHero(config["heroes.water"], Element.WATER)
        self.__initHero(config["heroes.earth"], Element.EARTH)
        self.__initHero(config["heroes.fire"], Element.FIRE)
        self.__initHero(config["heroes.light"], Element.LIGHT)
        self.__initHero(config["heroes.dark"], Element.DARK)

        settings = config["settings"]
        self.request = settings["request"]
        self.magicMedals = float(settings["mm"])
        self.magicMedalHero = settings["mmHero"]
        self.magicMedalsDaily = float(settings["mmDaily"])
        self.requestSunday = settings["requestSunday"]

    def __initHero(self, pool, element: Element):
        splitter = re.compile(' +')
        for key in pool:
            values = re.split(splitter, pool[key])
            stars = int(values[0])
            if stars < 7:
                rarity = Rarity.EPIC
                if len(values) > 2:
                    value = values[2]
                    if value == 'c':
                        rarity = Rarity.COMMON
                    elif value == 'r':
                        rarity = Rarity.RARE

                hero = Hero(name=key, stars=stars, medals=int(values[1]), rarity=rarity)
                self.heroes[element.value][hero.name] = hero

    def requestHero(self, heroes: dict, day: date):
        isSunday = day.isoweekday() == 7
        requestHero = self.request
        requestHeroSunday = self.requestSunday

        for hero in heroes.values():
            if hero.name == requestHero or hero.name == requestHeroSunday:
                hero.incrementRequest(isSunday)

    def incrementMagicMedal(self):
        self.magicMedals += self.magicMedalsDaily

    def useMagicMedals(self, heroes: dict):
        if not self.magicMedals.is_integer():
            return

        for hero in heroes.values():
            if hero.name == self.magicMedalHero:
                hero.incrementMagicMedals(self.magicMedals)
                self.magicMedals = 0
