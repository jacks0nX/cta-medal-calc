from calculator.Calculator import Calculator
from settings.SettingsUtils import SettingsUtils
from utils.DungeonUtils import DungeonUtils
from utils.EventUtils import EventUtils
from utils.HeroUtils import Element, HeroUtils

SettingsUtils.init()
DungeonUtils()
HeroUtils()
EventUtils()
calculator = Calculator()

for elementString in SettingsUtils.calcElements:
    element = Element(elementString)
    results = calculator.calculateMedals(element=element)
    calculator.print(results, element, sort=True, showHistory=SettingsUtils.showHistory)

input()
