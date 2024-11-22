
from models.substance import Substance

class Signal(Substance):

    def __init__(self, substance, emit, receive, triggerCombination, prodTime, spreadType, sendingSpeed, energyCosts, afterEffectTime, spreadSpeed=None):
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

        if self.spreadType == 'air':
            self.spreadSpeed = spreadSpeed

        self.active = False
        self.activeSignals = []
        self.radius = 0

    
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
