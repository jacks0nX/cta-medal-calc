import datetime
from configparser import ConfigParser
from typing import List

from common.models.Event import Event
from common.utils.CommonEventUtils import CommonEventUtils


class MedalEventUtils(CommonEventUtils):

    events: List[Event] = []

    def __init__(self, config: ConfigParser):
        startString = config.get("settings", "x2")
        self.events = self.init(startString, duration=2, daysOff=13)

    def isDoubleDungeon(self, day: datetime.date) -> bool:
        return self.isDay(day, self.events)
