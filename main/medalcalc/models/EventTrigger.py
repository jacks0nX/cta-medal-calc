

class EventTrigger:

    hero: str
    star: int
    oldValue: object
    newValue: object

    def __init__(self, value: str, oldValue=None):
        values = value.split("=")
        self.hero = values[0].strip()

        secondValue = values[1]
        if len(values) > 2:
            self.star = int(secondValue)
            self.newValue = values[2].strip()
        else:
            self.star = 7
            self.newValue = secondValue

        self.oldValue = oldValue
