
from collections import deque
import random

class EnemyCluster():
    
    def __init__(self, enemy, num, speed, position, grid):
        self.enemy = enemy
        self.num = num
        self.speed = speed
        self.position = position
        self.grid = grid
        self.stepCounter = 0
        

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
        #print(positions)
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
    
    
    def choosePlant(self, start):
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
        helperGrid = self.grid.helperGrid()
        pPos = self.detectPlant(helperGrid)
        shortestPaths = [] # Liste mit allen kürzesten Pfaden mit der gleichen Länge
        shortestPathLength = None
        
        if len(pPos) == 0:
            print('\nno plant. stop simulation')
            return []
        
        for plant in pPos:
            path = self.findShortestPath(start, plant)
            if path is not None:
                if shortestPathLength is None or len(path) < shortestPathLength: # Falls neuer kürzester Pfad gefunden wird, reset der Liste
                    shortestPathLength = len(path)
                    shortestPaths = [path]
                elif len(path) == shortestPathLength: # Kürzester Pfad mit gleicher Länge wird hinzugefügt
                    shortestPaths.append(path)
        
        if len(shortestPaths) > 0:
            return random.choice(shortestPaths) # Wähle einen zufälligen kürzesten Pfad aus der Liste
        else:
            return None
    

    def move(self):
        """_summary_
            Bestimmt die Schritte, um von der aktuellen Position zur nächsten Pflanze zu gelangen.
            Die Methode berechnet den kürzesten Pfad von der aktuellen Position ('self.position') zu einer Pflanze
            mithilfe der Methode 'findPlant'. Anschließend erstellt sie eine Liste von Schritten, die zur Pflanze führen,
            indem sie die aufeinanderfolgenden Positionen im Pfad durchläuft. Wenn kein Pfad gefunden wird, wird `None` zurückgegeben.

        Returns:
           list[tuple[int, int]] | None: Eine Liste von Positionen, die die Schritte zur Pflanze darstellen, oder 'None', wenn kein Pfad gefunden wurde.
        """
        start = self.position
        path = self.choosePlant(start)
        steps = []
        #print(start, path[1:])
        
        if path  == []:
            print('no path. stop simulation\n')
            return None
        
        for i in range(0, len(path)-1):
            nextPos = i + 1 
            steps.append(path[nextPos])

        #print(steps)
        return steps
    
    
    def eatPlant(self, ec, ePos, plant, pPos):
        # Prüfen, ob die Positionen übereinstimmen
        if ePos == pPos:
            grid = self.grid.getGrid()
            # Durchlaufe alle Objekte an der Position und entferne die Pflanze
            for plant in grid[pPos[0]][pPos[1]]:
                print(f'{ec.enemy.name} is eating {plant.name} at position {pPos}.')
                #grid[pPos[0]][pPos[1]].remove(obj)  # Entferne die spezifische Pflanze
                self.grid.removePlant(plant)  # Aktualisiere auch die Pflanzenliste im Grid
            
