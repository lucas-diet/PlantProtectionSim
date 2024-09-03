

class Simulation:

    def __init__(self, grid):
        self.grid = grid

    
    def runStep(self):
        for plant in self.grid.plants[:]:
            plant.grow()
            plant.survive()
            plant.reproduce()
    
    
    def run(self, steps):
        print('\n ##########################')
        print(' ###### initial grid ######')
        print(' ##########################\n')
        self.grid.display()
        print(' #################### \n')

        for _ in range(steps):
            if not self.grid.hasPlants():
                print('no more plants. simulation ending.')
                break

            self.runStep()
            self.grid.updateEnemyPos()
            #self.grid.display()
