

class Substance():

    def __init__(self, name, type):
        self.name = name
        self.type = type

    
    def getName(self):
        return self.name
    

    def getType(self):
        return self.type



class Signal(Substance):

    def __init__(self, substance, emit, receive, triggerCombination, prodTime, spreadType, sendingSpeed, energyCosts, afterEffectTime):
        super().__init__(name=substance.name, type=substance.type)
        self.substance = substance
        self.emit = emit
        self.receive = receive
        self.triggerCombination = triggerCombination
        self.prodTime = prodTime
        self.spreadType = spreadType
        self.sendingSpeed = sendingSpeed
        self.energyCosts = energyCosts
        self.afterEffectTime = afterEffectTime

        self.active = False
        self.activeSignals = []
        self.radius = {}

    
    def signalCosts(self, plant):
        plant.currEnergy -= self.energyCosts


    def activateSignal(self):
        if self not in self.activeSignals:
            self.active = True
            self.activeSignals.append(self)
        else:
            pass
    
    def deactivateSignal(self):
        if self in self.activeSignals:
            self.active = False
            self.activeSignals.remove(self)
        else:
            pass



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
        
        if not ec.currentPath:
            np = ec.newPathAfterDisplace(plant, self)
            if np:
                tp = np[-1]
            else:
                pass
    
        return np, tp
    

    def empoisonEnemies(self, ec):
        ec.intoxicated = True


    def killEnemies(self, ec):
        if ec.num > 0:
            ec.num -= self.eliminationStrength
