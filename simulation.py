

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
        for _ in range(steps):
            self.runStep()  
            self.grid.updateEnemiePos()
