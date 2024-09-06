

from models.plant import Plant
from models.enemy import Enemy
from models.grid import Grid

from controllers.simulation import Simulation

from views.gui import Gui

if __name__ == '__main__':
    grid = Grid(heigth=10, width=10)

    plantColor = ['#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']

    #species, initEnergy, growthRateEnegry, minEnegrgy, reproduction, offspingEnergy, minDist, maxDist, position, grid
    p1 = Plant(species='p1', 
               initEnergy=200, 
               growthRateEnegry=10, 
               minEnegrgy=50, 
               reproductionSteps=0, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2,
               position=(0, 5), 
               grid=grid,
               color=plantColor[0])
    
    p2 = Plant(species='p2', 
               initEnergy=100, 
               growthRateEnegry=5,
               minEnegrgy=50, 
               reproductionSteps=0, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2, 
               position=(4, 5), 
               grid=grid,
               color = plantColor[1])
    

    e1 = Enemy(species='e1', num=2, speed=2, position=(2,0), grid=grid)
    e2 = Enemy(species='e2', num=2, speed=1, position=(2,0), grid=grid)
    e3 = Enemy(species='e3', num=1, speed=1, position=(0,5), grid=grid)
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

    #e1.findPlant(e1.position)
    #e2.findPlant(e2.position)
    #e3.findPlant(e3.position)
    #e4.findPlant(e4.position)
    #e5.findPlant(e5.position)
    #e6.findPlant(e6.position)

    #e1.move()
    #e2.move()
    #e3.move()

    sim = Simulation(grid)
    sim.run()

    #gui = Gui()
    #gui.mainloop()