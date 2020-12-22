from random import randint
from typing import List

from MainSettings import MainSettings
from shardcalc.models.Awaken import Awaken
from common.utils.DateUtils import DateUtils
from shardcalc.utils.ShardEventUtils import CommonEventUtils, ShardEventUtils


class ShardUtils:

    __QUEST_COOLDOWN: int = 21
    __QUEST_REWARDS = [0, 150, 220, 320]

    __ARENA_SHARDS = {
        "L3": [240, 1200],
        "L2": [230, 1100],
        "L1": [220, 1000],
        "D3": [210, 9000],
        "D2": [190, 800],
        "D1": [170, 700]
    }

    __GW_CHEST_REWARD = 500

    eventUtils: CommonEventUtils

    shards: int
    shardsDaily: int

    daily: str
    season: str
    awakens: List[Awaken] = []
    questCooldowns = {}

    raidBoss: int

    gwScore: int
    gwKeys: int
    gwWinRate: int

    def __init__(self):
        config = MainSettings.config
        self.eventUtils = ShardEventUtils(config)

        self.shards = config.getint("settings", "shards")
        self.__processPacifier(config.get("settings", "pacifier"))

        self.shardsDaily = config.getint("settings", "artifact")

        # leagues
        self.daily = config.get("arena", "daily")
        self.season = config.get("arena", "season")

        # gw
        self.gwScore = config.getint("gw", "score")
        self.gwKeys = config.getint("gw", "keys")
        self.gwWinRate = config.getint("gw", "win")

        # quests
        self.questCooldowns[1] = config.getint("quest", "arena1")
        self.questCooldowns[2] = config.getint("quest", "arena2")
        self.questCooldowns[3] = config.getint("quest", "arena3")

        # raids
        self.raidBoss = config.getint("settings", "raidBoss")

        # awakens
        awakens = config["awakens"]
        for key in config["awakens"]:
            values: str = awakens[key]
            splitValues = values.split(" ")

            for value in splitValues:
                awaken = Awaken(key, int(value))
                self.awakens.append(awaken)

    def __processPacifier(self, pacifier: str):
        if len(pacifier) == 0:
            return

        pacifies = pacifier.split(",")
        for pacify in pacifies:
            pacifyFromTo = pacify.strip().split(" ")
            fromCost = Awaken.AWAKEN_COST[int(pacifyFromTo[0])]
            toCost = Awaken.AWAKEN_COST[int(pacifyFromTo[1])]
            self.shards += fromCost - toCost

    def getDailyShards(self, league: str):
        return self.__ARENA_SHARDS[league][0]

    def getSeasonShards(self, league: str):
        return self.__ARENA_SHARDS[league][1]

    def getArenaRewards(self) -> int:
        dailyLeague = self.daily[0]

        if DateUtils.isMonday():
            return 0

        if DateUtils.isTuesday():
            league = dailyLeague + "1"
            return self.getDailyShards(league)

        if DateUtils.isWednesday():
            league = dailyLeague + "2"
            if self.daily >= league:
                return self.getDailyShards(league)

        dailyShards = self.getDailyShards(self.daily)
        if DateUtils.isSunday():
            return self.getSeasonShards(self.season) + dailyShards
        return dailyShards

    def getQuestRewards(self) -> int:
        shards = 0

        for arenaQuest in range(1, 4):
            arena = self.questCooldowns[arenaQuest]
            if arena == 0:
                shards += self.__QUEST_REWARDS[arenaQuest]
                self.questCooldowns[arenaQuest] = self.__QUEST_COOLDOWN
            else:
                self.questCooldowns[arenaQuest] = arena - 1

        return shards

    def getGwRewards(self) -> int:
        if not DateUtils.isGwRewardDay():
            return 0

        randomNumber = randint(0, 100)
        isWin = randomNumber <= self.gwWinRate
        self.gwKeys += 3 if isWin else 1
        winLoseMult = 4 if isWin else 8

        # open chest
        chestShards = 0
        if self.gwKeys == 6:
            self.gwKeys -= 6
            chestShards = self.__GW_CHEST_REWARD

        return int(self.gwScore / winLoseMult) + chestShards

    def getRaidRewards(self) -> int:
        isOffDay = not self.eventUtils.isRaidDay(DateUtils.currentDate)
        if isOffDay:
            return self.raidBoss * 4
        return 0

    def getArtifactShards(self) -> int:
        return self.shardsDaily
