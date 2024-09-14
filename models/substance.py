

class Substance:

    def __init__(self, name, type, plantName):
        self.name = name
        self.type = type
        self.plantName = plantName

    
    def setName(self, name):
        self.name = name
    

    def setType(self, type):
        if type == 'messenger':
            self.type = type
        elif type == 'toxin':
            self.type = type