import configparser
import os
import tkinter
from enum import Enum
from tkinter.filedialog import askopenfilename


class CalculationType(Enum):
    MEDALS = "meals"
    SHARDS = "shards"

    def isMedalCalc(self):
        return self.value == self.MEDALS.value

    def isShardCalc(self):
        return self.value == self.SHARDS.value


class MainSettings:

    debugFile = 'medalcalc/settings.ini'

    calculationType: CalculationType

    config: configparser.ConfigParser = None

    @staticmethod
    def init():
        file = MainSettings.__readConfig(fileDialog=True)
        # file = MainSettings.__readConfig(fileName=MainSettings.debugFile)
        # file = MainSettings.__readConfig()

        if not file:
            input("A settings file could not be loaded.")
            raise Exception("Settings file could not be loaded")

        print(f"Using settings file: {file}")

        isMedalCalc = "dungeons" in MainSettings.config.sections()
        if isMedalCalc:
            MainSettings.calculationType = CalculationType.MEDALS
        else:
            MainSettings.calculationType = CalculationType.SHARDS

    @staticmethod
    def __readConfig(fileName: str = "", fileDialog: bool = False) -> str:
        path = fileName
        # path = MainSettings.debugFile

        # config = configparser.ConfigParser()
        # readInput = config.read(path)
        # if len(readInput) == 0:
        #     path = MainSettings.__readFile()
        #     config = configparser.ConfigParser()
        #     readInput = config.read(path)

        if fileDialog:
            path = MainSettings.__readFile()

        config = configparser.ConfigParser()
        readInput = config.read(path)
        if len(readInput) == 0:
            return ""

        MainSettings.config = config
        return os.path.basename(path)

    @staticmethod
    def __readFile():




        tkinter.Tk().withdraw()
        return tkinter.filedialog.askopenfilename(
            filetypes=[("Settings file", "*.ini")],
            title="Choose a settings file."
        )

    @staticmethod
    def isShardCalc():
        return MainSettings.calculationType.isShardCalc()

    @staticmethod
    def isMedalCalc():
        return MainSettings.calculationType.isMedalCalc()
