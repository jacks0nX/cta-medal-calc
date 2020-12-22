import random

from typing import List

from medalcalc.models.Hero import Hero
from medalcalc.models.RaidBoss import RaidBoss


class RaidEvent:

    boss: RaidBoss
    crusher: str
    heroes: List[str]

    def __init__(self, boss: RaidBoss, crusher: str, heroes: List[str]):
        self.boss = boss
        self.crusher = crusher
        self.heroes = heroes

    def incrementCrusher(self, heroes: List[Hero], medals: int):
        for hero in heroes:
            if hero.name == self.crusher:
                hero.increment(medals)

    def incrementRandomHero(self, heroes: List[Hero], medals: int):
        ccHeroes = self.heroes.copy()
        ccHeroes.append(self.crusher)

        heroName = random.choice(ccHeroes)
        for hero in heroes:
            if hero.name == heroName:
                hero.increment(medals)
