import configparser
import re
from collections import namedtuple
from typing import List

Event = namedtuple('Event', 'start end')


class SettingsUtils:

    CONFIG_PATH = "./settings/settings.ini"
    config = None

    calcElements: List[str] = []
    showHistory: bool

    @staticmethod
    def init():
        config = configparser.ConfigParser()
        config.read(SettingsUtils.CONFIG_PATH)
        SettingsUtils.config = config

        SettingsUtils.__initCalcs(config["calculator"])

    @staticmethod
    def __initCalcs(config):
        splitter = re.compile(' +')

        SettingsUtils.showHistory = config["showHistory"] == 'true'
        SettingsUtils.showHistory = config["showHistory"] == 'true'

        farmElements = re.split(splitter, config["elements"])
        for element in farmElements:
            SettingsUtils.calcElements.append(element)

