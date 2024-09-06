

class Simulation:

    def __init__(self, grid):
        self.grid = grid

    
    def runStep(self):
        for plant in self.grid.plants[:]:
            plant.grow()
            plant.survive()
            plant.reproduce()


    def initDisplay(self):
        print('\n##########################')
        print('###### initial grid ######')
        print('##########################\n')
        self.grid.displayGridEnergy()
        self.grid.displayEnemyNum()
        print()
        self.grid.displayGrid()
        print('#################### \n')


    def noPlantsBreak(self):
        if not self.grid.hasPlants():
            print('no more plants. simulation ending.')
            return True
        return False
    

    def upperGridEnergyBreak(self):
        if self.grid.getGridEnergy() > 1000:                #TODO: später umschreiben als Parameter
            print('Upper Border -- Grid-Energy')
            return True
        return False
    

    def upperEnemyNumBreak(self):
        if self.grid.getGridEnemyNum() > 10:                #TODO: später umschreiben als Parameter
            print('Upper Border -- Enemies')
            return True
        return False

    def run(self):
        self.initDisplay()
        count = 1
        while True:
            if self.noPlantsBreak():
                break
            
            if self.upperGridEnergyBreak():
                break

            if self.upperEnemyNumBreak():
                break

            self.runStep()
            print(count)
            self.grid.displayGridEnergy()
            self.grid.displayEnemyNum()
            self.grid.collectAndMoveEnemies()
            print('#################### \n')
            count += 1
