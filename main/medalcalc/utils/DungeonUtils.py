from datetime import date
from typing import List

from MainSettings import MainSettings
from medalcalc.models.EventTrigger import EventTrigger
from medalcalc.models.Hero import Hero
from common.utils.DateUtils import DateUtils
from medalcalc.utils.MedalEventUtils import MedalEventUtils
from medalcalc.utils.HeroUtils import Element


class DungeonUtils:

    DUNGEON_DAYS = {
        1: [Element.DARK, Element.FIRE],
        2: [Element.EARTH, Element.LIGHT],
        3: [Element.WATER, Element.FIRE],
        4: [Element.EARTH, Element.LIGHT],
        5: [Element.WATER, Element.DARK],
        6: [Element.FIRE, Element.LIGHT],
        7: [Element.WATER, Element.EARTH, Element.DARK]
    }

    weeklyDungeons = {
        "water": 0,
        "earth": 0,
        "fire": 0,
        "light": 0,
        "dark": 0
    }

    dailyDungeons = {
        "monday": "",
        "tuesday": "",
        "wednesday": "",
        "thursday": "",
        "friday": "",
        "saturday": "",
        "sunday": ""
    }


    eventUtils: MedalEventUtils

    ticketsDaily: int
    rebuysX2: int
    ticketsExtraX2: int

    elementX2: Element
    __elementX2events: List[EventTrigger] = []
    __weeklyDungeonEvents: List[EventTrigger] = []


    def __init__(self):
        config = MainSettings.config
        self.eventUtils = MedalEventUtils(config)
        weeklyDungeons = config["dungeons.weekly"]

        dungeons = config["dungeons"]
        self.__initTrigger(dungeons["x2"], weeklyDungeons)

        self.ticketsDaily = int(dungeons["daily"])
        self.rebuysX2 = int(dungeons["rebuys"])
        self.ticketsExtraX2 = int(dungeons["extraTickets"])

    def __initTrigger(self, x2Value: str, weeklyDungeons):
        values = x2Value.split(",")
        self.elementX2 = Element(values.pop(0))
        self.__elementX2events.clear()
        for splitValue in values:
            event = EventTrigger(splitValue)
            self.__elementX2events.append(event)

        self.__weeklyDungeonEvents.clear()
        for key in weeklyDungeons:
            value = weeklyDungeons[key]
            values = value.split(",")
            self.dailyDungeons[key] = values.pop(0)
            for splitValue in values:
                event = EventTrigger(splitValue, oldValue=key)
                self.__weeklyDungeonEvents.append(event)

    def checkEventTriggers(self, hero: Hero):
        for event in self.__elementX2events:
            if event.hero == hero.name and event.star == hero.stars:
                self.elementX2 = Element(event.newValue)

        for event in self.__weeklyDungeonEvents:
            if event.hero == hero.name and event.star == hero.stars:
                self.dailyDungeons[str(event.oldValue)] = str(event.newValue)

    def isDoubleDungeonDay(self, day: date, element: Element, elementX2: Element):
        if element is not elementX2:
            return False

        return self.eventUtils.isDoubleDungeon(day)

    def isDoubleDungeon(self, day: date):
        return self.eventUtils.isDoubleDungeon(day)

    def isDungeonDay(self, day: int, element: Element):
        dungeons = self.DUNGEON_DAYS[day]
        return element in dungeons

    def getFarmedDays(self, day: date, element: Element):
        weekDay = day.isoweekday()
        days = 0

        for i in range(1, weekDay):
            if self.isDungeonDay(i, element):
                days += 1
        return days

    def getDungeon(self) -> Element:
        dayName = DateUtils.dayname()
        return Element(self.dailyDungeons[dayName])

    def getElementsPerWeek(self, element: Element) -> int:
        count = 0
        for key in self.dailyDungeons:
            daily = self.dailyDungeons[key]
            if daily == element.value:
                count += 1
        return count

    def anyPerWeek(self, element: Element) -> bool:
        return self.getElementsPerWeek(element) > 0
