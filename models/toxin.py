
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

    def toxinCosts(self, plant):
        #print(f'[DEBUG]: pre Energy {plant.currEnergy}')
        plant.currEnergy -= self.energyCosts               # Produktion kostet energie 
        #print(f'[DEBUG]: post Energy {plant.currEnergy}')
        
    def displaceEnemies(self, ec, plant, toxin):
        if plant.isPoisonous == True and self.deadly == 'n':
            # TODO Feind weglenken von sich
            pass