

class Awaken:

    AWAKEN_COST = [
        0,
        10,
        50,
        250,
        1000,
        3000,
        10000,
        20000
    ]

    name: str
    awaken: int

    def __init__(self, name: str, awaken: int):
        self.name = name
        self.awaken = awaken

    def getCost(self) -> int:
        return self.AWAKEN_COST[self.awaken]
