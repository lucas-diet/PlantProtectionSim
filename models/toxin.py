
from models.substance import Substance

class Toxin(Substance):

    def __init__(self, substance, plantTransmitter, energyCosts, triggerCombination, prodTime, deadly, eliminationStrength, alarmDist):
        super().__init__(name=substance.name, type='toxin')
        self.substance = substance
        self.plantTransmitter = plantTransmitter
        self.energyCosts = energyCosts
        self.triggerCombination = triggerCombination
        self.prodTime = prodTime
        self.deadly = deadly
        self.eliminationStrength = eliminationStrength
        self.alarmDist = alarmDist
   

    def toxinCosts(self, plant):
        #print(f'[DEBUG]: pre Energy {plant.currEnergy}')
        plant.currEnergy -= self.energyCosts               # Produktion kostet energie 
        #print(f'[DEBUG]: post Energy {plant.currEnergy}')


    def displaceEnemies(self, ec, plant, allPlants):
        np = []
        tp = 0
        if len(ec.currentPath) == 0:
            np = ec.newPath(plant, allPlants)
            if len(np) > 0:
                tp = np[-1]
            else:
                tp = 0

        return np, tp
    

    def empoisonEnemies(self, ec):
        ec.intoxicated = True


    def killEnemies(self, ec):
        if ec.num > 0:
            ec.num -= self.eliminationStrength

            if ec.num <= 0:
                ec.num = 0
                ec.grid.removeEnemies(ec)