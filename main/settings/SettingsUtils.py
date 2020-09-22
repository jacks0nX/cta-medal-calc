import configparser
import os
import tkinter
from tkinter import *
from tkinter.filedialog import askopenfilename
from collections import namedtuple
from typing import List

Event = namedtuple('Event', 'start end')


class SettingsUtils:

    CONFIG_PATH = "settings.ini"
    DEFAULT_PATH = "defaultSettings.ini"

    debugFile = 'spooky.ini'

    config = None
    calcElements: List[str] = []
    showHistory: bool

    @staticmethod
    def init():
        file = SettingsUtils.__readConfig(fileDialog=True)
        # file = SettingsUtils.__readConfig(fileName=SettingsUtils.debugFile)

        if not file:
            input("A settings file could not be loaded.")
            raise Exception("Settings file could not be loaded")

        print(f"Using settings file: {file}")
        SettingsUtils.__initCalcs(SettingsUtils.config["calculator"])

    @staticmethod
    def __readConfig(fileName: str = "", fileDialog: bool = False) -> str:
        path = fileName
        if fileDialog:
            path = SettingsUtils.__readFile()

        config = configparser.ConfigParser()
        readInput = config.read(path)
        if len(readInput) == 0:
            return ""

        SettingsUtils.config = config
        return os.path.basename(path)

    @staticmethod
    def __readFile():
        tkinter.Tk().withdraw()
        return tkinter.filedialog.askopenfilename(
            filetypes=[("Settings file", "*.ini")],
            title="Choose a settings file."
        )

    @staticmethod
    def __initCalcs(config):
        SettingsUtils.showHistory = config["showHistory"] == 'true'
        SettingsUtils.showHistory = config["showHistory"] == 'true'

        farmElements = re.split(' +', config["elements"])
        for element in farmElements:
            SettingsUtils.calcElements.append(element)
