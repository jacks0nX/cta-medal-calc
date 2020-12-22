from MainSettings import MainSettings
from medalcalc.calculator.MedalCalculator import MedalCalculator
from shardcalc.calculator.ShardCalculator import ShardCalculator

MainSettings.init()


# shards
if MainSettings.isShardCalc():
    calculator = ShardCalculator()
    calculator.calculateShards()
    calculator.print()

# medals
if MainSettings.isMedalCalc():
    calculator = MedalCalculator()
    calculator.printSettings()
    calculator.calculateMedals()
    calculator.print(sort=True)


input()
