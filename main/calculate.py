import json

from calculator.Calculator import Calculator
from models.HeroHistory import HeroHistory
from settings.SettingsUtils import SettingsUtils
from utils.DungeonUtils import DungeonUtils
from utils.EventUtils import EventUtils
from utils.HeroUtils import Element, HeroUtils

SettingsUtils.init()
dungeonUtils = DungeonUtils()
heroUtils = HeroUtils()
EventUtils()
calculator = Calculator()


print(f"Settings")
HeroHistory.printFooter()
length = 25
print(f"Request (common):".ljust(length) + str(heroUtils.request))
print(f"Request (sunday):".ljust(length) + str(heroUtils.requestSunday))
print(f"MM Hero:".ljust(length) + str(heroUtils.magicMedalHero))
print(f"Element x2:".ljust(length) + dungeonUtils.elementX2.value)
print(f"Dungeon daily tickets:".ljust(length) + str(dungeonUtils.ticketsDaily))
print(f"Dungeon x2 extra tickets:".ljust(length) + str(dungeonUtils.ticketsExtraX2))
print(f"Dungeon x2 rebuys:".ljust(length) + str(dungeonUtils.rebuysX2))
print(f"Weekly dungeons:".ljust(length) + json.dumps(dungeonUtils.weeklyDungeons))
HeroHistory.printFooter()


for elementString in SettingsUtils.calcElements:
    element = Element(elementString)
    results = calculator.calculateMedals(element=element)
    calculator.print(results, element, sort=True, showHistory=SettingsUtils.showHistory)

input()


# - 400 medals thing
#