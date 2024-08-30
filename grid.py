
import numpy as np

from plant import Plant
from enemie import Enemie

class Grid():

    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth
        self.plants = []
        self.enemies = []
        self.grid = np.full((width, heigth), None)
       
    
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
                    print(f'{(cell.currEnergy / cell.initEnergy) * 100:.1f}% ', end='')
                elif isinstance(cell, Enemie):
                    print(f'{cell.species}-#{cell.num} ', end='')
                else:
                    print(' ---- ', end='')
            print()

        print('\n')


    def addEnemie(self, enemie):
        self.enemies.append(enemie)
        self.grid[enemie.position] = enemie

    
    def removeEnemie(self, enemie):
        self.enemies.remove(enemie)
        self.grid[enemie.position] = None


    def createTempGrid(self):
        grid = self.grid

        tmpGrid = []

        for i in range(0, len(grid)):
            row = []
            for j in range(0, len(grid[0])):
                if grid[i][j] is not None:
                    if isinstance(grid[i][j], Plant):
                        row.append('P')
                    elif isinstance(grid[i][j], Enemie):
                        row.append('E')
                else:
                    row.append('*')
            tmpGrid.append(row)

        return tmpGrid


    def detectEnemies(self):
        grid = self.grid

        enemiesPos = []
        for i in range(0, len(grid)):
           
            for j in range(0, len(grid[0])):
                if isinstance(grid[i][j], Enemie):
                    enemiesPos.append((i,j))
        
        return enemiesPos


            