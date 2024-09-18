
from models.substance import Substance

class Toxin(Substance):

    def __init__(self, substance, plantTransmitter, energyCosts, triggerCombination, prodTime, deadly, eliminationStrength, alarmDist):
        super().__init__(name=substance.name, type='toxin')
        self.substance = substance
        self.plantTransmitter = plantTransmitter
        self.energyCosts = energyCosts
        self.triggerCombination = triggerCombination
        self.prodTime = prodTime
        self.prodCounter = 0
        self.deadly = deadly
        self.eliminationStrength = eliminationStrength
        self.alarmDist = alarmDist