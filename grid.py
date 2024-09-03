
import numpy as np

from plant import Plant
from enemy import Enemy

class Grid():

    def __init__(self, heigth, width):
        self.heigth = heigth
        self.width = width
        self.plants = []
        self.enemys = []
        self.grid = np.full((heigth, width), None)
       
    
    def addPlant(self, plant):
        self.plants.append(plant)
        self.grid[plant.position] = plant

    
    def removePlant(self, plant):
        self.plants.remove(plant)
        self.grid[plant.position] = None


    def isOccupied(self, position):
        return self.grid[position] is not None


    def isWithinBounds(self, x, y):
        return 0 <= x < self.heigth and 0 <= y < self.width
    

    def connectPlants(self, pos1, pos2):
        plant1 = self.grid[pos1]
        plant2 = self.grid[pos2]

        # TODO: Symbiose von zwei Pflanzen


    def addEnemy(self, enemy):
        self.enemys.append(enemy)
        self.grid[enemy.position] = enemy

    
    def removeEnemy(self, enemy):
        self.enemys.remove(enemy)
        self.grid[enemy.position] = None


    def helperGrid(self):
        grid = self.grid
        hGrid = []
        
        for i in range(0, len(grid)):
            row = []
            for j in range(0, len(grid[0])):
                if grid[i][j] is not None:
                    if isinstance(grid[i][j], Plant):
                        row.append('P')
                    elif isinstance(grid[i][j], Enemy):
                        row.append('E')
                else:
                    row.append('*')
            hGrid.append(row)

        return hGrid
    

    def display(self):
        for row in self.grid:
            for cell in row:
                if isinstance(cell, Plant):
                    print(f' {(cell.currEnergy / cell.initEnergy) * 100:.1f}% ', end='')
                elif isinstance(cell, Enemy):
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
    

    def updateEnemyPos(self):
        for i, row in enumerate(self.grid):
            for j, enemy in enumerate(row):
                if isinstance(enemy, Enemy):
                    oldPos = (i,j)
                    steps = enemy.move()
                    newPos = oldPos

                    if steps is None:
                        continue
                    
                    for step in steps:
                        tmpPos = (step[0], step[1])
                        if 0 <= tmpPos[0] < len(self.grid) and 0 <= tmpPos[1] < len(self.grid[0]):
                            newPos = tmpPos
                            break
                    
                    if oldPos != newPos:
                        if isinstance(self.grid[newPos[0]][newPos[1]], Enemy):
                            # TODO: Logik dafür, dass Freinde auf dem gleichen Feld gleichzeitig sitzen können, ohne sich zu fressen
                            pass
                        self.grid[oldPos[0]][oldPos[1]] = None
                        self.grid[newPos[0]][newPos[1]] = enemy
                        enemy.position = newPos

                        print(f' {enemy.species} moved from {oldPos} to {newPos} \n')
                        self.display()
                        print(' #################### \n')
                        break
                                         

                    
                    