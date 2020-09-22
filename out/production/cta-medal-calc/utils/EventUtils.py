import datetime
from collections import namedtuple
from typing import List

from settings.SettingsUtils import SettingsUtils

Event = namedtuple('Event', 'start end')


class EventUtils:

    X2_DAYS = 500

    eventsX2: List[Event] = []

    def __init__(self):
        config = SettingsUtils.config["settings"]
        startString = config["x2"]
        start = datetime.datetime.strptime(startString, '%Y-%m-%d')

        for n in range(self.X2_DAYS):
            end = start + datetime.timedelta(days=2)
            event = Event(start.date(), end.date())
            self.eventsX2.append(event)
            start = start + datetime.timedelta(days=16)

    def isDoubleDungeon(self, day: datetime.date) -> bool:
        for x2Day in self.eventsX2:
            if x2Day.start <= day <= x2Day.end:
                return True

        return False
