

class AirConnection():

    def __init__(self, senderPlant):
        self.senderPlant = senderPlant

        self.radius = 0
        self.receiverPlants = []
        self.connectedWith = [False for _ in range(0, len(self.receiverPlants))]

    
    def getCurrentRadius(self):
        return self.radius



    