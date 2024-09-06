
import numpy as np

from models.plant import Plant
from models.enemy import Enemy

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
        return 0 <= x < self.heigth and 0 <= y < self.width
    

    def getGridEnergy(self):
        energy = 0
        for plant in self.plants:
            energy += plant.currEnergy
        return energy
    

    def displayGridEnergy(self):
        print(f'Grid-Energy: {self.getGridEnergy()}')

    
    def getGridEnemyNum(self):
        enemyNum = 0
        for enemy in self.enemies:
            enemyNum += enemy.num
        return enemyNum
    

    def displayEnemyNum(self):
        print(f'Enemy-Number: {self.getGridEnemyNum()}')


    def connectPlants(self, pos1, pos2):
        plant1 = self.grid[pos1]
        plant2 = self.grid[pos2]

        # TODO: Symbiose von zwei Pflanzen


    def addEnemy(self, enemy):
        self.enemies.append(enemy)
        if isinstance(self.grid[enemy.position], list):
            self.grid[enemy.position].append(enemy)
        else:
            self.grid[enemy.position] = [enemy]

    
    def removeEnemy(self, enemy):
        self.enemies.remove(enemy)
        if isinstance(self.grid[enemy.position], list):
            self.grid[enemy.position].remove(enemy)
            if len(self.grid[enemy.position]) == 0:
                self.grid[enemy.position] = None


    def helperGrid(self):
        grid = self.grid
        hGrid = []
        
        for i in range(0, len(grid)):
            row = []
            for j in range(0, len(grid[0])):
                if grid[i][j] is not None:
                    if isinstance(grid[i][j], list) and any(isinstance(e, Enemy) for e in grid[i][j]):
                        row.append('E')
                    elif isinstance(grid[i][j], Plant):
                        row.append('P')                
                else:
                    row.append('*')
            hGrid.append(row)
        return hGrid
    

    def displayGrid(self):
        # Bestimme die maximale Anzahl an Feinden in einem Feld für das Layout
        max_enemies_in_cell = max(len(cell) if isinstance(cell, list) else 1 for row in self.grid for cell in row)     
        
        for row in self.grid:
            for level in range(max_enemies_in_cell):
                for cell in row:
                    if isinstance(cell, list):
                        if level < len(cell):
                            enemy = cell[level]
                            print(f'{enemy.species}-#{enemy.num} ', end='  ')
                        else:
                            print(' ' * 8, end=' ')  # Leeren Platz lassen, wenn kein Feind auf dieser Ebene
                    elif isinstance(cell, Plant) and level == 0:
                        # Pflanzen nur auf der ersten Ebene darstellen
                        print(f'{(cell.currEnergy / cell.initEnergy) * 100:.1f}%', end='  ')
                    elif cell is None and level == 0:
                        print('------ ', end=' ')
                    else:
                        print(' ' * 8, end=' ')  # Leeren Platz lassen
                print()  # Neue Zeile nach jeder Ebene
            print()  # Zusätzliche neue Zeile nach jeder Zeile im Grid
        

    def hasPlants(self):
        for row in self.grid:
            for plant in row:
                if isinstance(plant, Plant):
                    return True  # Eine Pflanze gefunden, also gibt es noch Pflanzen
        return False
    
    
    def displayMove(self, enemy, oldPos, newPos):
        print(f'{enemy.species} moved from {oldPos} to {newPos}\n')

    
    def getNewPosition(self, steps):
        for step in steps:
            newPos = (step[0], step[1])
            if self.isWithinBounds(newPos[0], newPos[1]):
                return newPos
        return None


    def updateEnemyPosition(self, enemy, oldPos, newPos):
        # Entferne den Feind von der alten Position
            if isinstance(self.grid[oldPos[0]][oldPos[1]], list):
                self.grid[oldPos[0]][oldPos[1]].remove(enemy)

                if len(self.grid[oldPos[0]][oldPos[1]]) == 0:
                    self.grid[oldPos[0]][oldPos[1]] = None
            else:
                self.grid[oldPos[0]][oldPos[1]] = None

            # Füge den Feind zur neuen Position hinzu
            if isinstance(self.grid[newPos[0]][newPos[1]], list):
                self.grid[newPos[0]][newPos[1]].append(enemy)
            else:
                self.grid[newPos[0]][newPos[1]] = [enemy]

            # Aktualisiere die Position des Feindes
            enemy.position = newPos


    def moveEachEnemy(self, moveArr):
        # Bewege jeden Feind
        for enemy, oldPos in moveArr:
            if enemy.stepCounter < enemy.speed - 1:
                enemy.stepCounter += 1
                newPos = oldPos
            else:
                enemy.stepCounter = 0
                steps = enemy.move()
                tmpPos = oldPos

                if steps is None:
                    continue
                
                if self.getNewPosition(steps) is not None:
                    newPos = self.getNewPosition(steps) 
                else:
                    newPos = tmpPos

                if oldPos != newPos:
                    self.updateEnemyPosition(enemy, oldPos, newPos)
                  
            self.displayMove(enemy, oldPos, newPos)
            self.displayGrid()
                

    def collectAndMoveEnemies(self):
        # Erstelle eine Liste von Feinden mit ihren Positionen
        enemies_to_move = []

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if isinstance(cell, list):
                    for enemy in cell:
                        enemies_to_move.append((enemy, (i, j)))
                elif isinstance(cell, Enemy):
                    enemies_to_move.append((cell, (i, j)))

        self.moveEachEnemy(enemies_to_move)
                
                                        

                    
                    