from enum import Enum


class Rarity(Enum):
    COMMON = "common"
    RARE = "rare"
    EPIC = "epic"

    def isCommon(self):
        return self == self.COMMON

    def isRare(self):
        return self == self.RARE

    def isEpic(self):
        return self == self.EPIC

    def getGuildCoins(self) -> int:
        if self.isCommon():
            return 100
        if self.isRare():
            return 200
        if self.isEpic():
            return 1000
