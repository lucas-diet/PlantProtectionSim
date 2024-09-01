

class Simulation:

    def __init__(self, grid):
        self.grid = grid

    
    def runStep(self):
        for plant in self.grid.plants[:]:
            plant.grow()
            plant.survive()
            plant.reproduce()
    
    
    def run(self, steps):
        self.grid.display()
        print(' -------------------- \n\n')
        for _ in range(steps):
            
            if self.grid.hasPlants() == False:
                break
            else:
                print(_)
                self.runStep()
                self.grid.updateEnemiePos()
                self.grid.display()
