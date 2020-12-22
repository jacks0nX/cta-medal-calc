import datetime
from typing import List

from common.models.Event import Event


class CommonEventUtils:

    DEFAULT_DAYS = 500

    def init(self, startString: str, duration: int, daysOff: int, days=DEFAULT_DAYS, content=None) -> List[Event]:
        events = []
        start = datetime.datetime.strptime(startString, '%Y-%m-%d')

        for n in range(days):
            end = start + datetime.timedelta(days=duration)
            event = Event(start.date(), end.date())

            if content:
                count = n % (len(content))
                event.content = content[count]

            events.append(event)
            start = end + datetime.timedelta(days=daysOff + 1)

        return events

    def isDay(self, day: datetime.date, events: List[Event]) -> bool:
        return any(event.isBetween(day) for event in events)
