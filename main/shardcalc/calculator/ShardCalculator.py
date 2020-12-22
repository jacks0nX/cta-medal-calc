from datetime import date
from typing import List

from shardcalc.models.AwakenHistory import AwakenHistory
from common.utils.DateUtils import DateUtils
from shardcalc.utils.ShardUtils import ShardUtils


class ShardCalculator:

    TIMEOUT_DAYS: int = 5000

    shardUtils: ShardUtils
    shards: int
    result: List[AwakenHistory] = []

    def __init__(self):
        self.shardUtils = ShardUtils()

    def calculateShards(self):
        # dates
        DateUtils.init(date.today())

        # shards
        self.shards = self.shardUtils.shards

        while True:
            # arena
            self.shards += self.shardUtils.getArenaRewards()

            # GW
            self.shards += self.shardUtils.getGwRewards()

            # quests
            self.shards += self.shardUtils.getQuestRewards()

            # raids
            self.shards += self.shardUtils.getRaidRewards()

            # artifact
            self.shards += self.shardUtils.getArtifactShards()

            # awaken
            self.__processAwaken()
            if len(self.shardUtils.awakens) == 0:
                return
            ########

            # next day
            DateUtils.nextDay()

            # timeout
            if DateUtils.days > self.TIMEOUT_DAYS:
                raise Exception(f"Timeout after {self.TIMEOUT_DAYS} days: {DateUtils.days}")
            ###############

    def __processAwaken(self):
        awaken = self.shardUtils.awakens[0]
        if self.shards >= awaken.getCost():
            self.shards -= awaken.getCost()
            self.shardUtils.awakens.remove(awaken)
            history = AwakenHistory(awaken.name, DateUtils.currentDate, DateUtils.days, awaken.awaken)
            self.result.append(history)

    def print(self):
        AwakenHistory.printHeader("")

        for result in self.result:
            result.print()

        AwakenHistory.printFooter()
