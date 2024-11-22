
import random

class Plant():

    def __init__(self, name, initEnergy, growthRateEnegry, minEnegrgy, reproductionIntervall, offspingEnergy, minDist, maxDist, position, grid, color):
        self.name = name
        self.initEnergy = initEnergy
        self.currEnergy = initEnergy
        self.growthRateEnegry = growthRateEnegry
        self.minEnergy = minEnegrgy
        self.reproductionIntervall = reproductionIntervall
        self.offspringEnergy = offspingEnergy
        self.minDist = minDist
        self.maxDist = maxDist
        self.position = position
        self.grid = grid
        self.color = color[int(self.name[1])-1]
        
        self.age = 0
        self.gridConnections = {}

        #self.isAlarmed_signal = False
        self.signalAlarms = {}
        #self.isSignaling = False
        self.isSignalSignaling = {}

        self.signalProdCounters = {}
        self.signalSendingCounters = {}
        self.afterEffectTime = 0
        self.afterEffectTimes = {}

        #self.isAlarmed_toxin = False
        self.toxinAlarms = {}
        #self.isToxic = False
        self.isToxically = {}

        self.toxinProdCounters = {} #dict, wo produktionsCounter für jedes [ec, toxin] gespeichert wird.

    def grow(self):
        self.currEnergy += self.initEnergy * (self.growthRateEnegry / 100)
        self.age += 1


    def survive(self):
        if self.currEnergy < self.minEnergy:
            self.grid.removePlant(self)
            
        
    def scatterSeed(self):
        if self.reproductionIntervall == 0:
            pass

        elif self.age % self.reproductionIntervall == 0:
            for _ in range(random.randint(1, 4)):       ## Zufall zwischen 1 und 4              # Wie viele Kinder soll es max geben?
                offspringPosition = self.setOffspringPos()
                
                if offspringPosition:
                    energyInput = input('Init-Energy of offspring:')                        # Input() famit Energie für jedes Nachkommen individuell ist
                    offspringEnergy = float(energyInput) if energyInput else 100            # default ist 100 Einheiten
                    offspring = Plant(name=self.name, 
                                      initEnergy=self.offspringEnergy, 
                                      growthRateEnegry=self.growthRateEnegry, 
                                      minEnegrgy=self.minEnergy, 
                                      reproductionIntervall=self.reproductionIntervall, 
                                      offspingEnergy=offspringEnergy,
                                      minDist=self.minDist, 
                                      maxDist=self.maxDist, 
                                      position=offspringPosition, 
                                      grid=self.grid,
                                      color=self.color
                    )
                    self.grid.addPlant(offspring)


    def getDirections(self):
        directions = []
        for dx in range(-self.maxDist, self.maxDist+1):
            for dy in range(-self.maxDist, self.maxDist+1):
                dist = abs(dx) + abs(dy)
                if self.minDist <= dist <= self.maxDist:
                    directions.append((dx, dy))
        
        return directions
    

    def setOffspringPos(self):        
        directions = self.getDirections()
        random.shuffle(directions)

        for dx, dy in directions:
            newX, newY = self.position[0] + dx, self.position[1] + dy

            if self.grid.isWithinBounds(newX, newY):
                if not self.grid.isOccupied((newX, newY)):
                    print(f'[DEBUG]: {self.name} auf {self.position} erzeugt Nachkommen auf {newX, newY}')
                    return (newX, newY)
                else:
                    print(f'[DEGUB]: Position {newX, newY} ist belegt. Nachkomme wird nicht erzeugt.')
                    pass
            else:
                print(f'[DEBUG]: Position {newX, newY} liegt außerhalb der Grenzen.')
                pass
            
        return None


    def getColor(self):
        print(self.color)
        return self.color

    
    def resetSignalProdCounter(self, ec, signal):
        self.signalProdCounters[ec, signal] = 0


    def incrementSignalProdCounter(self, ec, signal):
        key = (ec, signal)
        if key in self.signalProdCounters:
            self.signalProdCounters[ec, signal] += 1
        else:
            self.signalProdCounters[ec, signal] = 1


    def getSignalProdCounter(self, ec, signal):
        key = (ec, signal)
        return self.signalProdCounters.get(key, 0)
    

    def resetSignalSendCounter(self, ec, signal, rPlant):
        self.signalSendingCounters[ec, signal, rPlant] = 0


    def incrementSignalSendCounter(self, ec, signal, rPlant):
        key = (ec, signal, rPlant)
        if key in self.signalSendingCounters:
            self.signalSendingCounters[ec, signal, rPlant] += 1
        else:
            self.signalSendingCounters[ec, signal, rPlant] = 1

    
    def isSignalAlarmed(self, signal):
        return self.signalAlarms.get(signal, False)
    

    def setSignalAlarm(self, signal, status):
        self.signalAlarms[signal] = status

        # Wenn kein Signalalarm aktiv ist, setze `isSignaling` auf True
        #if any(self.signalAlarms.values()) == False:
        #    self.isSignaling = True
        #else:
        #    self.isSignaling = False


    def isSignalPresent(self, signal):
        return self.isSignalSignaling.get(signal, False)
    

    def setSignalPresence(self, signal, status):
        self.isSignalSignaling[signal] = status

        if any(self.isSignalSignaling.values()) == False:
            self.isSignaling = False
        else:
            self.isSignaling = True

    
    def enemySignalAlarm(self, toxin):      
        self.setSignalAlarm(toxin, True)
    

    def makeSignal(self, signal):
        self.setSignalAlarm(signal, False)
        self.setSignalPresence(signal, True)


    def setAfterEffectTime(self, signal, aft):
        self.afterEffectTimes[self, signal] = aft

    
    def getAfterEffectTime(self, signal):
        key = (self, signal)
        return self.afterEffectTimes.get(key, 0)

    
    def resetToxinProdCounter(self, ec, toxin):
        self.toxinProdCounters[ec, toxin] = 0


    def incrementToxinProdCounter(self, ec, toxin):
        key = (ec, toxin)
        if key in self.toxinProdCounters:
            self.toxinProdCounters[ec, toxin] += 1
        else:
            self.toxinProdCounters[ec, toxin] = 1


    def getToxinProdCounter(self, ec, toxin):
        key = (ec, toxin)
        return self.toxinProdCounters.get(key, 0)
    

    def isToxinAlarmed(self, toxin):
        return self.toxinAlarms.get(toxin, False)
    

    def setToxinAlarm(self, toxin, status):
        self.toxinAlarms[toxin] = status

        #if any(self.toxinAlarms.values()) == False:
        #    self.isAlarmed_toxin = True
        #else:
        #    self.isAlarmed_toxin = False


    def isToxinPresent(self, toxin):
        return self.isToxically.get(toxin, False)
    

    def setToxinPresence(self, toxin, status):
        self.isToxically[toxin] = status

        if any(self.isToxically.values()) == False:
            self.isToxic = False
        else:
            self.isToxic = True

    
    def enemyToxinAlarm(self, toxin):
        self.setToxinAlarm(toxin, True)
    

    def makeToxin(self, toxin):
        self.setToxinAlarm(toxin, False)
        self.setToxinPresence(toxin, True)


    def getSignalSendCounter(self, ec, signal, rPlant):
        key = (ec, signal, rPlant)
        return self.signalSendingCounters.get(key, 0)
    

    def sendSignal(self, rplant, signal):
        rplant.setSignalPresence(signal, True)

    
    def airSpreadSignal(self, ec, signal):
        if self.isSignalPresent(signal) == True:
            print(f'[DEBUG]: {self.name} verbreitet {signal.name} via Luft')