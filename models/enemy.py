
from collections import deque
import random

class Enemy():
    
    def __init__(self, species, num, speed, position, grid):
        self.species = species
        self.num = num
        self.speed = speed
        self.position = position
        self.grid = grid

    def detectPlant(self, grid):
        pos = (0,0)
        posistions = []

        for i in range(0, len(grid)):
            for j in range(0,len(grid[0])):
                if grid[i][j] == 'P':
                    pos = (i,j)
                    posistions.append(pos)
                else:
                    pass
        
        return posistions
    

    def findShortPath(self, grid, start, goal):
        """_summary_
            Breadth First Search
        Args:
            grid (_type_): _description_
            start (_type_): _description_
            goal (_type_): _description_

        Returns:
            _type_: _description_
        """
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
    
    
    def findPlant(self, start):
        helperGrid = self.grid.helperGrid()
        pPos = self.detectPlant(helperGrid)
        shortestPaths = [] # Liste mit allen kürzesten Pfaden mit der gleichen Länge
        shortestPathLength = None

        if len(pPos) == 0:
            print('no plant. stop simulation')
            return []
        
        for plant in pPos:
            path = self.findShortPath(helperGrid, start, plant)
            if path is not None:
                pathLength = len(path)
                if shortestPathLength is None or pathLength < shortestPathLength: # Falls neuer kürzester Pfad gefunden wird, reset der Liste
                    shortestPathLength = pathLength
                    shortestPaths = [path]
                elif pathLength == shortestPathLength: # Kürzester Pfad mit gleicher Länge wird hinzugefügt
                    shortestPaths.append(path)
        
        if len(shortestPaths) > 0:
            return random.choice(shortestPaths) # Wähle einen zufälligen kürzesten Pfad aus der Liste
        else:
            return None
        
    
    def move(self):
        start = self.position
        path = self.findPlant(start)
        print(path)
        steps = []
        #print(start, path[1:])

        if path  == []:
            print('no path. stop simulation\n')
            return None
        
        for i in range(0, len(path)-1, self.speed):
            if i + self.speed < len(path) - 1:
                nextPos = i + self.speed
                steps.append(path[nextPos])  
            else:
                nextPos = len(path) - 1
                steps.append(path[nextPos])
        #print(steps)
        return steps