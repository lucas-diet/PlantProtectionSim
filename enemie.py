
from collections import deque

class Enemie():
    
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
        tmpGrid = self.grid.createTempGrid()
        pPos = self. detectPlant(tmpGrid)

        #print('EP: ', ePos)
        #print('PP: ', pPos)

        if len(pPos) == 0:
            #print('Keine Pflanze gefunden!')
            return None
            
        shortWay = None
        for plantPos in pPos:
            path = self.findShortPath(tmpGrid, start, plantPos)
            if path:
                if shortWay is None or len(path) < len(shortWay):
                    shortWay = path
            
        if len(shortWay) > 0:
            #print('\nKürzester Weg gefunden:')
            #for step in shortWay:
            #    print(step, end='')
            #print()
            return shortWay
        else:
            print('\nKein Pfad gefunden.')
            return None
        

    def movement(self):

        start = self.position
        path = self.findPlant(start)
        steps = []

        if path is None:
            #print('Keine Pflanze gefunden!')
            return []

        for i in range(0, len(path), self.speed): 
            if i + self.speed < len(path) - 1:
                nextPos = i + self.speed
                #print(f'{path[nextPos]}')
                steps.append(path[nextPos])
            else:
                nextPos = len(path) - 1
                #print(f'{path[nextPos]}')
            
            if path[nextPos] not in steps:
                steps.append(path[nextPos])

            if nextPos in steps:
                pass

            if nextPos == len(path) - 1:
                break
        
        #print('steps: ', steps)
        return steps
    

        
        

        
        