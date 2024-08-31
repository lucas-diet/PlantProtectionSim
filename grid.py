
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
    

    def isWithinBounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.heigth
    

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
        print('\n')

    def hasPlants(self):
        for row in self.grid:
            for cell in row:
                if isinstance(cell, Plant):
                    return True  # Eine Pflanze gefunden, also gibt es noch Pflanzen
        return False

    def updateEnemiePos(self):
        #self.display()
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if isinstance(cell, Enemie):
                    oldPos = (i, j)
                    steps = cell.movement()
                    newPos = oldPos
                    for step in steps:
                        #print(step)
                        tmpPos = (step[0], step[1])
                        #print(newPos)
                        if 0 <= tmpPos[0] < len(self.grid) and 0 <= tmpPos[1] < len(self.grid[0]):
                            newPos = tmpPos
                            break
                        else:
                            newPos = oldPos
                    # Setze die neue Position
                    if oldPos != newPos:
                        self.grid[oldPos[0]][oldPos[1]] = None  # Entferne den Feind von der alten Position
                        self.grid[newPos[0]][newPos[1]] = cell  # Setze den Feind auf die neue Position
                        cell.position = newPos  # Aktualisiere die Position des Feinds im Objekt
                        print(f'Enemy {cell.species} moved from {oldPos} to {newPos}\n')
                        
                    else:
                        #print(f'Enemy at {oldPos} did not move.')
                        if not isinstance(cell, Plant):
                            break
                    self.display()
                    break


            