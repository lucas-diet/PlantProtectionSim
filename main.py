

from plant import Plant
from enemie import Enemie
from grid import Grid
from simulation import Simulation

if __name__ == '__main__':
    grid = Grid(width=5, heigth=5)

    #species, initEnergy, growthRateEnegry, minEnegrgy, reproduction, offspingEnergy, minDist, maxDist, position, grid
    p1 = Plant(species='P1', 
               initEnergy=100, 
               growthRateEnegry=10, 
               minEnegrgy=50, 
               reproductionSteps=0, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2, 
               position=(2, 2), 
               grid=grid)
    
    p2 = Plant(species='P2', 
               initEnergy=100, 
               growthRateEnegry=10, 
               minEnegrgy=50, 
               reproductionSteps=0, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2, 
               position=(2, 4), 
               grid=grid)
    # species, num, speed, position, grid
    e1 = Enemie(species='E1', num=4, speed=2, position=(1,0), grid=grid)
    e2 = Enemie(species='E2', num=1, speed=1, position=(4,4), grid=grid)

    grid.addPlant(p1)
    grid.addPlant(p2)
    grid.addEnemie(e1)
    grid.addEnemie(e2)

    e1.findPlant(grid.createTempGrid(), e1.position)
    e2.findPlant(grid.createTempGrid(), e2.position)

    #print(grid.detectEnemies())

    #e1.movement((1,1), e1.speed, e1.position, p1.position)
    #grid.addEnemie(e1)

    sim = Simulation(grid)
    #sim.run(steps=10)