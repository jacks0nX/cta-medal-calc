from typing import Optional, List

from MainSettings import MainSettings
from common.models.Event import Event
from common.utils.CommonEventUtils import CommonEventUtils
from common.utils.DateUtils import DateUtils
from medalcalc.models.Hero import Hero
from medalcalc.models.RaidBoss import RaidBoss
from medalcalc.models.RaidEvent import RaidEvent


class RaidEventUtils(CommonEventUtils):

    ROTATION = {
        RaidBoss.SAMURAI: RaidEvent(RaidBoss.SAMURAI, "furiosa", ["leaf blade", "dark knight", "gold knight", "magmus", "chaos"]),
        RaidBoss.TWIN_FACE: RaidEvent(RaidBoss.TWIN_FACE, "seraph", ["alda", "dark hunter", "arcana", "kage", "neko"]),
        RaidBoss.MAD_KING: RaidEvent(RaidBoss.MAD_KING, "atlantus", ["onyx", "pirato", "rufus", "spyro", "joan of arc"]),
        RaidBoss.GUNLORD: RaidEvent(RaidBoss.GUNLORD, "one eye", ["kasumi", "kasai", "jasmine", "kage", "luka"]),
        RaidBoss.FROSTWING: RaidEvent(RaidBoss.FROSTWING, "groovine", ["thorn", "dark wolf", "oceana", "robin hood", "krouki"]),
        RaidBoss.ASTROLAB: RaidEvent(RaidBoss.ASTROLAB, "sorrow", ["scud", "rufus", "krouki", "monki mortar", "dark hunter"])
    }

    CC_TIER = {
        1: [10, 80],
        2: [30, 100, 20],
        3: [50, 100, 80],
        4: [80, 100, 100, 70],
        5: [120, 100, 100, 100, 100, 10]
    }

    events: List[Event] = []
    tiers: dict = {}

    def __init__(self):
        config = MainSettings.config
        startString = config.get("raid", "samuraiStart")
        self.events = self.init(startString, duration=2, daysOff=1, content=list(self.ROTATION.values()))

        for raid in self.ROTATION.values():
            value = config.get("raid", raid.boss.value)
            if value and int(value) > 0:
                self.tiers[raid.boss] = value


    def isEvent(self, name: RaidBoss):
        event = self.getRaidEvent()
        return event and event.content.boss == name

    def isEventStart(self, name: RaidBoss):
        event = self.getRaidEvent()
        return event and event.content.boss == name and event.start == DateUtils.currentDate

    def getRaidEvent(self) -> Optional[Event]:
        for event in self.events:
            isRaidDay = event.isBetween(DateUtils.currentDate)
            if isRaidDay:
                return event

    def crusherChest(self, heroes: List[Hero]):
        for tier in self.tiers.items():
            isRaidDay = self.isEventStart(tier[0])
            if isRaidDay:
                self.getMedals(heroes, tier[0], int(tier[1]))

    def getMedals(self, heroes: List[Hero], name: RaidBoss, maxTier: int):
        rotation = self.ROTATION.get(name)

        for tier in range(1, maxTier):
            tierMedals = self.CC_TIER.get(tier).copy()

            rotation.incrementCrusher(heroes, tierMedals.pop(0))
            for medals in tierMedals:
                rotation.incrementRandomHero(heroes, medals)
