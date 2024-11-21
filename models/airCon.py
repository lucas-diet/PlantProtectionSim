

class AirConnection:

    def __init__(self, senderPlant):
        self.senderPlant = senderPlant
        
        self.receiverPlants = []
        self.connected = [False for _ in range(0, len(self.receiverPlants))]

    