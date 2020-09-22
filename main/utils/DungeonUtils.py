from datetime import date
from typing import List

from settings.SettingsUtils import SettingsUtils
from utils.EventUtils import EventUtils
from utils.HeroUtils import Element


class Event:



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

    eventUtils: EventUtils

    ticketsDaily: int
    rebuysX2: int
    elementX2: Element
    ticketsExtraX2: int

    __elementX2events: List[Event]

    def __init__(self):
        self.eventUtils = EventUtils()

        config = SettingsUtils.config
        weeklyDungeons = config["dungeons.weekly"]
        for key in weeklyDungeons:
            self.weeklyDungeons[key] = int(weeklyDungeons[key])

        dungeons = config["dungeons"]
        self.elementX2 = Element(dungeons["x2"])
        self.ticketsDaily = int(dungeons["daily"])
        self.rebuysX2 = int(dungeons["rebuys"])
        self.ticketsExtraX2 = int(dungeons["extraTickets"])

    def isDoubleDungeonDay(self, day: date, element: Element, elementX2: Element):
        if element is not elementX2:
            return False

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


