

from plant import Plant
from enemy import Enemy
from grid import Grid
from simulation import Simulation

if __name__ == '__main__':
    grid = Grid(heigth=10, width=10)

    #species, initEnergy, growthRateEnegry, minEnegrgy, reproduction, offspingEnergy, minDist, maxDist, position, grid
    p1 = Plant(species='P1', 
               initEnergy=100, 
               growthRateEnegry=0, 
               minEnegrgy=50, 
               reproductionSteps=0, 
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
               position=(4, 5), 
               grid=grid)
    
    e1 = Enemy(species='E1', num=2, speed=3, position=(0,0), grid=grid)
    e2 = Enemy(species='E2', num=2, speed=1, position=(3,3), grid=grid)
    e3 = Enemy(species='E3', num=1, speed=1, position=(3,3), grid=grid)
    #e4 = Enemie(species='E4', num=1, speed=5, position=(4,1), grid=grid)
    #e5 = Enemie(species='E5', num=1, speed=5, position=(2,1), grid=grid)
    #e6 = Enemie(species='E6', num=1, speed=5, position=(4,1), grid=grid)

    grid.addPlant(p1)
    grid.addPlant(p2)
    
    grid.addEnemy(e1)
    grid.addEnemy(e2)
    #grid.addEnemy(e3)
    #grid.addEnemy(e4)
    #grid.addEnemy(e5)
    #grid.addEnemy(e6)

    #hGrid = grid.helperGrid()

    #e1.findPlant(e1.position)
    #e2.findPlant(e2.position)
    #e3.findPlant(e3.position)
    #e4.findPlant(e4.position)
    #e5.findPlant(e5.position)
    #e6.findPlant(e6.position)

    #e1.move()
    #e2.move()
    #e3.move()
    #grid.updateEnemyPos()

    sim = Simulation(grid)
    sim.run(20)