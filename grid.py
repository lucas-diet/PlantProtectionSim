
import numpy as np

from plant import Plant
from enemie import Enemie

class Grid():

    def __init__(self, heigth, width):
        self.heigth = heigth
        self.width = width
        self.plants = []
        self.enemies = []
        self.grid = np.full((heigth, width), None)
       
    
    def addPlant(self, plant):
        self.plants.append(plant)
        self.grid[plant.position] = plant

    
    def removePlant(self, plant):
        self.plants.remove(plant)
        self.grid[plant.position] = None


    def isOccupied(self, position):
        return self.grid[position] is not None
    
    def isOccupiedEnemie(self, x, y):
        return isinstance(self.grid[x][y], Enemie)

    def isWithinBounds(self, x, y):
        return 0 <= x < self.heigth and 0 <= y < self.width
    

    def connectPlants(self, pos1, pos2):
        plant1 = self.grid[pos1]
        plant2 = self.grid[pos2]

        # Symbiose von zwei Pflanzen


    def addEnemie(self, enemie):
        self.enemies.append(enemie)
        self.grid[enemie.position] = enemie

    
    def removeEnemie(self, enemie):
        self.enemies.remove(enemie)
        self.grid[enemie.position] = None


    def helperGrid(self):
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
    

    def display(self):
        for row in self.grid:
            for cell in row:
                if isinstance(cell, Plant):
                    print(f' {(cell.currEnergy / cell.initEnergy) * 100:.1f}% ', end='')
                elif isinstance(cell, Enemie):
                    print(f' {cell.species}-#{cell.num}  ', end='')
                else:
                    print(' ------ ', end='')
            print()
        print()


    def hasPlants(self):
        for row in self.grid:
            for plant in row:
                if isinstance(plant, Plant):
                    return True  # Eine Pflanze gefunden, also gibt es noch Pflanzen
        return False
    

    def updateEnemiePos(self):
        #idxs = []
        new_positions = {}
        for i, row in enumerate(self.grid):
            for j, enemie in enumerate(row):
                if isinstance(enemie, Enemie):
                    oldPos = (i,j)
                    steps = enemie.move()
                    newPos = oldPos
                    #print(steps)

                    if steps is None:
                        continue

                    count = []
                    
                    for idx, step in enumerate(steps):
                        tmpPos = (step[0], step[1])
                        if 0 <= tmpPos[0] < len(self.grid) and 0 <= tmpPos[1] < len(self.grid[0]):
                            newPos = tmpPos
                            #idxs.append(idx)
                            break

                    if newPos not in new_positions:
                        new_positions[newPos] = enemie
                    
                    if oldPos != newPos:
                        self.grid[oldPos[0]][oldPos[1]] = None
                        self.grid[newPos[0]][newPos[1]] = enemie
                        enemie.position = newPos

                        print(f'{enemie.species} moved from {oldPos} to {newPos} \n')
                        self.display()
                        break
                        #print(len(idxs)+1, ' #################### \n') 
                                         

                    
                    