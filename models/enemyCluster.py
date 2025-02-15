
from collections import deque
import random
import numpy as np

from models.plant import Plant

class Enemy():

    def __init__(self, name):
        self.name = name

    
    def getName(self):
        return self.name
    


class EnemyCluster():
    
    def __init__(self, enemy, num, speed, position, grid, eatVictory, eatingSpeed):
        self.enemy = enemy
        self.num = num
        self.speed = speed
        self.position = position
        self.grid = grid
        self.eatVictory = eatVictory
        self.eatingSpeed = eatingSpeed
        
        self.stepCounter = 0
        self.eatedEnergy = 0
        self.newBorns = 0
        self.targetPlant = None
        self.currentPath = []
        self.intoxicated = False
        self.lastVisitedPlants = {}
        self.lastPlant = None
        self.circle_id = None

    
    def insertLastVisits(self, plant, signal):
        if signal is not None:
            key = (plant, signal)  # Verwende den kombinierten Schlüssel aus Pflanze und Signal
            self.lastVisitedPlants[key] = signal.afterEffectTime
        else:
            self.lastVisitedPlants[(plant, None)] = 0  # Standardwert setzen, wenn kein Signal übergeben wurde


    def deleteLastVisits(self, plant, signal):
        keys_to_remove = [(p, s) for (p, s) in self.lastVisitedPlants if p == plant and s == signal]
        for key in keys_to_remove:
            self.lastVisitedPlants.pop(key, None)


    def getAfterEffectTime(self, plant, signal):
        key = (plant, signal)  # Verwende den kombinierten Schlüssel aus Pflanze und Signal
        return self.lastVisitedPlants.get(key, signal.afterEffectTime)


    def isPlantInLastVisits(self, plant):
        return any(key[0] == plant for key in self.lastVisitedPlants.keys())

 
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
    

    def dynamicDirections(self, currPos, directions, goal):
        """
            Berechnet eine dynamische Reihenfolge für die Bewegungsrichtungen, 
            basierend auf der Nähe zum Ziel ohne Priorisierung der Achsen.
            Dabei berechnet sie die quadratische euklidische Distanz zu jedem potenziellen Nachbarn des aktuellen Punktes.
            """
        return sorted(directions, key=lambda d: (currPos[0] + d[0] - goal[0]) ** 2 + (currPos[1] + d[1] - goal[1]) ** 2)

    
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

            for direction in self.dynamicDirections(currPos, directions, goal):
                nextRow = currPos[0] + direction[0]
                nextCol = currPos[1] + direction[1]
                nextPos = (nextRow, nextCol)

                if 0 <= nextRow < rows and 0 <= nextCol < cols and nextPos not in distances:
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
        if self.targetPlant is not None:
            # Alle aktuellen Pflanzenpositionen abrufen
            current_plants = self.detectPlant(self.grid.helperGrid())
            
            # Überprüfen, ob die Zielpflanze noch existiert
            if self.targetPlant not in current_plants:  
                self.targetPlant = None  # Zielpflanze zurücksetzen
            else:
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
    

    def checkAndUpdatePath(self, currentPos):
        """
        Überprüft, ob eine nähere Pflanze vorhanden ist, und aktualisiert den Pfad des Feindes.
        Die zuletzt besuchte Pflanze wird bei der Auswahl ausgeschlossen.
        """
        # Überprüfe alle Pflanzen im Grid
        helperGrid = self.grid.helperGrid()
        plantPositions = self.detectPlant(helperGrid)

        if not plantPositions:
            return  # Keine Pflanzen vorhanden

        # Finde die nächstgelegene Pflanze
        nearestPlant = None
        shortestDistance = float('inf')

        for plantPos in plantPositions:
            # Hole das Pflanzenobjekt an der entsprechenden Position
            plant = self.grid.getPlantAt(plantPos)

            if plant == self.lastPlant:
                continue
            
            distance = np.abs(plantPos[0] - currentPos[0]) + np.abs(plantPos[1] - currentPos[1])  # Manhatten-Distanz
            if distance < shortestDistance:
                shortestDistance = distance
                nearestPlant = plantPos

        # Falls eine nähere Pflanze gefunden wurde und sie nicht die letzte besuchte Pflanze ist, aktualisiere den Pfad
        if nearestPlant and nearestPlant != self.targetPlant:
            newPath = self.findShortestPath(currentPos, nearestPlant)
            if newPath:
                self.path = newPath
                self.targetPlant = nearestPlant  # Aktualisiere das Ziel


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
        
    
    def eatPlant(self, ec, plant):
        # Prüfen, ob die Positionen übereinstimmen
        grid = self.grid.getGrid()
        hGrid = self.grid.helperGrid()
        ePos = ec.position
        pPos = plant.position
        
        if ePos == pPos and 'P' in hGrid[ePos[0]][ePos[1]]:
            plant = None
            for p in grid[pPos[0]][pPos[1]]:
                if isinstance(p, Plant):
                    plant = p
                    break

            if plant is not None:
                plant.currEnergy -= self.eatingSpeed
                self.eatedEnergy += self.eatingSpeed

                if plant.currEnergy < plant.minEnergy:
                    self.targetPlant = None
                    self.grid.removePlant(plant)

            self.notifyPlantEaten(pPos)

            # Jetzt ein neues Ziel suchen
            return self.chooseRandomPlant(ePos)
        
        else:
            self.grid.log.append(f'keine Pflanze an Position {pPos} gefunden')
            #print(f'[INfO]: keine Pflanze an Position {pPos} gefunden')


    def notifyPlantEaten(self, pPos):
        # Signalisiere allen Feinden, dass eine Pflanze gegessen wurde
        if self.targetPlant is None:
            for enemyCluster in self.grid.enemies:
                if enemyCluster.targetPlant == pPos:
                    enemyCluster.targetPlant = None  # Zurücksetzen des Ziels bei anderen Feinden
                    self.grid.log.append(f'{enemyCluster.enemy.name} hat sein Ziel verloren und schaut nach einer neuen Pflanze')
                    #print(f'[DEBUG]: {enemyCluster.enemy.name} hat sein Ziel verloren und schaut nach einer neuen Pflanze')
             

    def reproduce(self):
        if self.eatedEnergy >= self.eatVictory:
            self.newBorns += int(self.eatedEnergy / self.eatVictory)
            self.num += self.newBorns
            self.eatedEnergy -= self.newBorns * self.eatVictory  # Energie für neue Feinde abziehen
            self.newBorns = 0


    def newPathAfterDisplace(self, plant, toxin):
        if plant.isToxinPresent(toxin) == True:
            shortestDistance = float('inf')

            alternativePlants = self.filterUnblockedPlants(plant, toxin)

            # Suche nach Pflanzen mit der kürzesten Entfernung
            for p in alternativePlants:
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
                self.grid.log.append(f'{self.enemy.name} Keine alternative Pflanze gefunden!')
                #print(f'[DEBUG]: {self.enemy.name} Keine alternative Pflanze gefunden!')
                return []
        else:
            return None
            
    
    def filterUnblockedPlants(self, plant, toxin):
        """
        Filtere die Pflanzen, die nicht durch das Toxin blockiert sind.
        """
        unblockedPlants = [
            p for p in self.grid.plants
            if not p.isToxinPresent(toxin)  # Prüfen, ob die Pflanze durch das Toxin blockiert ist
            and p != plant  # Die Pflanze darf nicht die aktuelle sein
            and all(tox.name != toxin.name for tox in p.isToxically.keys())  # Toxin darf nicht von den Blockierenden Toxinen der Pflanze sein
        ]

        # Wenn keine unblockierten Pflanzen gefunden wurden, alle Pflanzen zurückgeben
        if not unblockedPlants:
            unblockedPlants = self.grid.plants

        return unblockedPlants



