

class SymbioticConnection():

    def __init__(self, plant1, plant2):
        self.plant1 = plant1
        self.plant2 = plant2

        self.connect = False


    def getDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


    def createConnection(self):
        self.connect = True
        pos1 = self.plant1.position
        pos2 = self.plant2.position
        dist = self.getDistance(pos1, pos2)

        if dist == 1 and self.connect:
            key1 = (self.plant1, self.plant2)
            key2 = (self.plant2, self.plant1)
            self.plant1.gridConnections[key1] = pos1, pos2
            self.plant2.gridConnections[key2] = pos2, pos1
        else:
            if dist > 1:
                print(f'[INFO]: {self.plant1.name} und {self.plant2.name} sind nicht benachbart')
            if self.connect == False:
                print(f'[INFO]: Keine Verbindung zwischen {self.plant1.name} und {self.plant2.name}')
    
        
