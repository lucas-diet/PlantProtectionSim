
from models.substance import Substance

class Toxin(Substance):

    def __init__(self, substance, plantTransmitter, energyCosts, triggerCombination, prodTime, deadly, eliminationStrength):
        super().__init__(name=substance.name, type=substance.type)
        self.substance = substance
        self.plantTransmitter = plantTransmitter
        self.energyCosts = energyCosts
        self.triggerCombination = triggerCombination
        self.prodTime = prodTime
        self.deadly = deadly
        self.eliminationStrength = eliminationStrength
   

    def toxinCosts(self, plant):
        plant.currEnergy -= self.energyCosts               # Produktion kostet energie


    def displaceEnemies(self, ec, plant):
        np = []
        tp = None
        
        if len(ec.currentPath) == 0:
            np = ec.newPath(plant, self)
            if len(np) > 0:
                tp = np[-1]
            else:
                pass
                tp = None
    
        return np, tp
    

    def empoisonEnemies(self, ec):
        ec.intoxicated = True


    def killEnemies(self, ec):
        if ec.num > 0:
            ec.num -= self.eliminationStrength

            if ec.num <= 0:
                ec.num = 0
                ec.lastToxin = None
                ec.grid.removeEnemies(ec)