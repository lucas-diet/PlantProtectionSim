
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
        
    def displaceEnemies(self, ec, plant, grid):

        #TODO: Wenn deadly == n, dann geht Feind auf dem nuen Pfad weiter, geht dann aber wieder zurück -> eine art endlosschleife

        if self.deadly == 'n' and plant.isPoisonous == True:
            newPath = ec.newPath(plant, grid.plants)
            print(newPath)
            #TODO: Logik dafür, dass der Feind von der Pflanze weggelenkt wird.