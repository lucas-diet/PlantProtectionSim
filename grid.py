
import numpy as np

from plant import Plant as plant

class Grid():

    def __init__(self, width, height):
        self.width = width
        self.heigth = height
        self.plants = []
        self.grid = np.full((width, height), None)

    
    def addPlant(self, plant):
        self.plants.append(plant)
        self.grid[plant.position] = plant

    
    def removePLant(self, plant):
        self.plants.remove(plant)
        self.grid[plant.position] = None


    def isOccupied(self, position):
        return self.grid[position] is not None
    

    def isWithinBounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.heigth
    

    def connectPLants(self, pos1, pos2):
        plant1 = self.grid[pos1]
        plant2 = self.grid[pos2]

        if plant1 and plant2:
            # Implementiere die Symbiose-Logik und zeichne die Verbindung
            pass

    def display(self):
        for row in self.grid:
            print(' '.join(f'{(plant.currEnergy / plant.initEnergy) * 100:.1f}%' if plant else '----' for plant in row))

        print('\n')