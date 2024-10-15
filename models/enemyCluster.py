
from collections import deque
import random

from models.plant import Plant

class EnemyCluster():
    
    def __init__(self, enemy, num, speed, position, grid, eatingSpeed, eatVictory):
        self.enemy = enemy
        self.num = num
        self.speed = speed
        self.position = position
        self.grid = grid
        self.stepCounter = 0
        self.eatVictory = eatVictory
        self.eatedEnergy = 0
        self.eatingSpeed = eatingSpeed
        self.newEnemy = 0
        self.targetPlant = None
        self.currentPath = []
        self.intoxicated = False
        self.lastVisitedPlant = None
        
     
    def detectPlant(self, grid):
        """_summary_
            Ermittelt die Positionen von Pflanzen im Grid.
            Die Methode durchsucht das übergebene Gitter `grid` nach Zellen, die durch 'P' 
            repräsentiert werden, und sammelt deren Positionen in einer Liste 'positions'.
            Diese Liste wird anschließend zurückgegeben.

        Args:
            grid (_type_): _description_

        Returns:
            Liste: Liste von Positionen, woe Pflanzen stehen
        """
        pos = (0,0)
        positions = []

        for i in range(0, len(grid)):
            for j in range(0,len(grid[0])):
                if 'P' in grid[i][j]:
                    pos = (i,j)
                    positions.append(pos)
                else:
                    pass
        return positions
    

    def findShortestPath(self, start, goal):
        """_summary_
            Finde den kürzesten Pfad zwischen zwei Punkten im Gitter mittels Breitensuche (BFS).
            Die Methode verwendet die Breitensuche, um den kürzesten Weg von 'start' nach 'goal' im übergebenen 'grid' zu ermitteln.
            Sie durchläuft die Nachbarzellen in den vier Hauptrichtungen (oben, unten, links, rechts) und verfolgt die bisher gefundenen Wege,
            um den kürzesten Pfad zu bestimmen. Der Pfad wird als Liste von Koordinaten zurückgegeben. 
            Wenn kein Pfad gefunden wird, wird 'None' zurückgegeben.

        Args:
             grid (list[list]): Das Gitter, in dem der Pfad gefunden werden soll.
                start (tuple[int, int]): Die Startposition im Gitter.
                goal (tuple[int, int]): Die Zielposition im Gitter.


        Returns:
            list[tuple[int, int]] | None: Eine Liste von Koordinaten, die den kürzesten Pfad darstellen, oder 'None', wenn kein Pfad gefunden wurde.
        """
        grid = self.grid.getGrid()
        rows, cols = len(grid), len(grid[0])
        directions = [(-1,0), (1,0), (0,-1), (0,1)] # Bewegungsmöglichkeiten: Oben, Unten, Links, Rechts

        queue = deque([start])
        distances = {start: 0}
        previous = {start: None}

        while len(queue) != 0:
            currPos = queue.popleft()

            if currPos == goal:
                path = []
                while currPos:
                    path.append(currPos)
                    currPos = previous[currPos]
                return path[::-1]

            for direction in directions:
                nextRow = currPos[0] + direction[0]
                nextCol = currPos[1] + direction[1]
                nextPos = (nextRow, nextCol)

                if 0 <= nextRow < rows and 0 <= nextCol < cols and nextPos not in distances:
                    #print(currPos, f'::{currPos}+{direction} =' , nextPos)
                    queue.append(nextPos)
                    distances[nextPos] = distances[currPos] + 1
                    previous[nextPos] = currPos
        return None
    
    
    def chooseRandomPlant(self, start):
        """_summary_
            Findet den kürzesten Pfad zu einer Pflanze im Grid, beginnend von einer Startposition.
            Die Methode durchsucht das Gitter nach Pflanzen, berechnet den kürzesten Pfad von 'start' zu jeder Pflanze
            mithilfe der Funktion 'findShortestPath' und sammelt alle Pfade mit der minimalen Länge. 
            Falls mehrere Pfade der gleichen kürzesten Länge existieren, wird zufällig einer ausgewählt und zurückgegeben.
            Wenn keine Pflanzen im Gitter gefunden werden, wird eine leere Liste zurückgegeben.

        Args:
            start (tuple[int, int]): Die Startposition im Grid.

        Returns:
            list[tuple[int, int]] | None: Der kürzeste Pfad zu einer Pflanze als Liste von Koordinaten oder 'None'
        """
        
        # Wenn bereits eine Zielpflanze gesetzt ist, muss keine neue ausgewählt werden
        if self.targetPlant is not None:
            return self.findShortestPath(start, self.targetPlant)
        
        helperGrid = self.grid.helperGrid()
        pPos = self.detectPlant(helperGrid)
        shortestPaths = [] # Liste mit allen kürzesten Pfaden mit der gleichen Länge
        shortestPathLength = None
        
        if len(pPos) == 0:
            print('\nno plant. stop simulation')
            return []
        
        for pos in pPos:
            path = self.findShortestPath(start, pos)
            if path is not None:
                if shortestPathLength is None or len(path) < shortestPathLength: # Falls neuer kürzester Pfad gefunden wird, reset der Liste
                    shortestPathLength = len(path)
                    shortestPaths = [path]
                elif len(path) == shortestPathLength: # Kürzester Pfad mit gleicher Länge wird hinzugefügt
                    shortestPaths.append(path)
        
        if len(shortestPaths) > 0:
            # Wähle eine zufällige Pflanze aus und speichere diese als Ziel
            chosenPath = random.choice(shortestPaths)
            self.targetPlant = chosenPath[-1]  # Letztes Element des Pfads ist das Ziel
            return chosenPath
        else:
            return None
    
    
    def getPath(self, start):
        return self.chooseRandomPlant(start)


    def move(self, path):
        """_summary_
            Bestimmt die Schritte, um von der aktuellen Position zur nächsten Pflanze zu gelangen.
            Die Methode berechnet den kürzesten Pfad von der aktuellen Position ('self.position') zu einer Pflanze
            mithilfe der Methode 'findPlant'. Anschließend erstellt sie eine Liste von Schritten, die zur Pflanze führen,
            indem sie die aufeinanderfolgenden Positionen im Pfad durchläuft. Wenn kein Pfad gefunden wird, wird `None` zurückgegeben.

        Returns:
           list[tuple[int, int]] | None: Eine Liste von Positionen, die die Schritte zur Pflanze darstellen, oder 'None', wenn kein Pfad gefunden wurde.
        """
        steps = []

        if path is None:
            print('no path. stop simulation\n')
            return None
        else:
            for i in range(1, len(path)):
                steps.append(path[i])

        return steps
        
    
    def eatPlant(self, ec, ePos, plant, pPos):
        # Prüfen, ob die Positionen übereinstimmen
        grid = self.grid.getGrid()
        hGrid = self.grid.helperGrid()
        
        if ePos == pPos and 'P' in hGrid[ePos[0]][ePos[1]]:
            plant = None
            for p in grid[pPos[0]][pPos[1]]:
                if isinstance(p, Plant):
                    plant = p
                    break

            if plant is not None:
                print(f'{ec.enemy.name} is eating {plant.name} at position {pPos}')
                plant.currEnergy -= self.eatingSpeed
                self.eatedEnergy += self.eatingSpeed

                if plant.currEnergy <= plant.minEnergy:
                    self.targetPlant = None
                    self.grid.removePlant(plant)

            # Signalisiere allen Feinden, dass eine Pflanze gegessen wurde
            if self.targetPlant is None:
                for enemyCluster in self.grid.enemies:
                    if enemyCluster.targetPlant == pPos:
                        enemyCluster.targetPlant = None  # Zurücksetzen des Ziels bei anderen Feinden
                        print(f'{enemyCluster.enemy.name} has lost its target and will look for a new plant')

            # Jetzt ein neues Ziel suchen
            return self.chooseRandomPlant(ePos)
        
        else:
            print(f'No plant found at position {pPos}.')
                    

    def reproduce(self):
        if self.eatedEnergy >= self.eatVictory:
            self.newEnemy += 1
            self.num += self.newEnemy
            self.eatedEnergy -= self.newEnemy * self.eatedEnergy
            self.newEnemy = 0


    def newPath(self, plant, allPlants):
        if plant.isToxic:
            alternativePlants = []
            shortestDistance = float('inf')

            # Suche nach Pflanzen mit der kürzesten Entfernung
            for p in allPlants:
                dist = self.grid.getDistance(self.position, p.position)

                if dist < shortestDistance and self.position != p.position:
                    # Neue kürzeste Distanz gefunden, leere Liste und füge diese Pflanze hinzu
                    shortestDistance = dist
                    alternativePlants = [p]
                elif dist == shortestDistance and self.position != p.position:
                    # Pflanze hat die gleiche kürzeste Distanz, also füge sie zur Liste hinzu
                    alternativePlants.append(p)

            if alternativePlants:
                # Wähle zufällig eine der Pflanzen mit der kürzesten Distanz
                alternativePlant = random.choice(alternativePlants)
                # Berechne den kürzesten Pfad zur gewählten Pflanze
                np = self.findShortestPath(self.position, alternativePlant.position)
                return np
            else:
                print('[DEBUG]: Keine alternative Pflanze gefunden!')
                return []
        else:
            return None