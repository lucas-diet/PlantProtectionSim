

from plant import Plant
from enemie import Enemie
from grid import Grid
from simulation import Simulation

if __name__ == '__main__':
    grid = Grid(heigth=5, width=6)

    #species, initEnergy, growthRateEnegry, minEnegrgy, reproduction, offspingEnergy, minDist, maxDist, position, grid
    p1 = Plant(species='P1', 
               initEnergy=100, 
               growthRateEnegry=10, 
               minEnegrgy=50, 
               reproductionSteps=5, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2, 
               position=(0, 5), 
               grid=grid)
    
    p2 = Plant(species='P2', 
               initEnergy=100, 
               growthRateEnegry=0, 
               minEnegrgy=50, 
               reproductionSteps=0, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2, 
               position=(2, 4), 
               grid=grid)
    
    # species, num, speed, position, grid
    e1 = Enemie(species='E1', num=2, speed=2, position=(0,0), grid=grid)
    #e2 = Enemie(species='E2', num=1, speed=5, position=(4,4), grid=grid)
    #e3 = Enemie(species='E3', num=1, speed=5, position=(3,3), grid=grid)
    #e4 = Enemie(species='E4', num=1, speed=5, position=(4,1), grid=grid)
    #e5 = Enemie(species='E5', num=1, speed=5, position=(2,1), grid=grid)
    #e6 = Enemie(species='E6', num=1, speed=5, position=(4,1), grid=grid)

    grid.addPlant(p1)
    grid.addPlant(p2)
    
    grid.addEnemie(e1)
    #grid.addEnemie(e2)
    #grid.addEnemie(e3)
    #grid.addEnemie(e4)
    #grid.addEnemie(e5)
    #grid.addEnemie(e6)
    tmpGrid = grid.createTempGrid()

    e1.findPlant(e1.position)
    #e2.findPlant(e2.position)
    #e3.findPlant(e3.position)
    #e4.findPlant(e4.position)
    #e5.findPlant(e5.position)
    #e6.findPlant(e6.position)

    #steps = e1.movement()
    #print(steps)
    #grid.updateEnemiePos(e1)

    #e1.movement((1,1), e1.speed, e1.position, p1.position)
    #grid.addEnemie(e1)

    sim = Simulation(grid)
    sim.run(100)