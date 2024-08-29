

from plant import Plant
from enemie import Enemie
from grid import Grid
from simulation import Simulation

if __name__ == '__main__':
    grid = Grid(width=5, height=5)
    #species, initEnergy, growthRateEnegry, minEnegrgy, reproduction, offspingEnergy, minDist, maxDist, position, grid
    p1 = Plant(species='P1', 
               initEnergy=100, 
               growthRateEnegry=10, 
               minEnegrgy=50, 
               reproductionSteps=5, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2, 
               position=(2, 2), 
               grid=grid)
    
    # species, num, speed, position, grid
    e1 = Enemie(species='E1', num=4, speed=2, position=(1,4), grid=grid)

    grid.addPlant(p1)
    grid.addEnemie(e1)

    sim = Simulation(grid)
    sim.run(steps=10)