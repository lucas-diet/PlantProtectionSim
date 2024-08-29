
import numpy as np

from plant import Plant
from enemie import Enemie

class Grid():

    def __init__(self, width, height):
        self.width = width
        self.heigth = height
        self.plants = []
        self.enemies = []
        self.grid = np.full((width, height), None)
    
    def addPlant(self, plant):
        self.plants.append(plant)
        self.grid[plant.position] = plant

    
    def removePlant(self, plant):
        self.plants.remove(plant)
        self.grid[plant.position] = None


    def isOccupied(self, position):
        return self.grid[position] is not None
    

    def isWithinBounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.heigth
    

    def connectPlants(self, pos1, pos2):
        plant1 = self.grid[pos1]
        plant2 = self.grid[pos2]

        # Symbiose von zwei Pflanzen

    def display(self):

        for row in self.grid:
            for cell in row:
                if isinstance(cell, Plant):
                    print(f'{(cell.currEnergy / cell.initEnergy) * 100:.1f}%', end =' ')
                elif isinstance(cell, Enemie):
                    print(f'{cell.species}', end=' ')
                else:
                    print('----', end=' ')
            print()

            #print(f'{(enemie.species)}' if enemie else '----' for enemie in row)

        print('\n')


    def addEnemie(self, enemie):
        self.enemies.append(enemie)
        self.grid[enemie.position] = enemie