

class Simulation:

    def __init__(self, grid):
        self.grid = grid

    
    def runStep(self):
        for plant in self.grid.plants[:]:
            plant.grow()
            plant.survive()
            plant.reproduce()
    
    
    def run(self):
        print('\n##########################')
        print('###### initial grid ######')
        print('##########################\n')
        self.grid.displayGridEnergy()
        print()
        self.grid.displayGrid()
        print('#################### \n')

        while True:
            if not self.grid.hasPlants():
                print('no more plants. simulation ending.')
                break
               
            self.runStep()
            self.grid.displayGridEnergy()
            self.grid.collectAndMoveEnemies()
            print('#################### \n')
