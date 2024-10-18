
from models.substance import Substance

class Signal(Substance):

    def __init__(self, substance, emit, receive, triggerCombination, spreadType, sendingSpeed, energyCosts, afterEffectTime):
        super().__init__(name=substance.name, type='signal')
        self.substance = substance
        self.emit = emit
        self.receive = receive
        self.triggerCombination = triggerCombination
        self.spreadType = spreadType
        self.sendingSpeed = sendingSpeed
        self.energyCosts = energyCosts
        self.afterEffectTime = afterEffectTime

        
        self.active = False
        self.activSignals = []

    
    def signalCosts(self, plant):
        plant.currentEnergy -= self.signalCosts

