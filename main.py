
from models.plant import Plant
from models.enemyCluster import EnemyCluster
from models.grid import Grid

from controllers.simulation import Simulation

from views.gui import Gui

if __name__ == '__main__':
    grid = Grid(height=6, width=6)

    plantColor = ['#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']

    #name, initEnergy, growthRateEnegry, minEnegrgy, reproduction, offspingEnergy, minDist, maxDist, position, grid
    p1 = Plant(name='p1', 
               initEnergy=200, 
               growthRateEnegry=10, 
               minEnegrgy=50, 
               reproductionIntervall=0, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2,
               position=(0, 3), 
               grid=grid,
               color=plantColor[0])
    
    p2 = Plant(name='p2', 
               initEnergy=100,
               growthRateEnegry=5,
               minEnegrgy=50, 
               reproductionIntervall=0, 
               offspingEnergy=60, 
               minDist=1, 
               maxDist=2, 
               position=(4, 3), 
               grid=grid,
               color = plantColor[1])
    

    e1 = EnemyCluster(name='e1', num=2, speed=3, position=(2,0), grid=grid)
    e2 = EnemyCluster(name='e2', num=2, speed=1, position=(0,3), grid=grid)
    e3 = EnemyCluster(name='e3', num=1, speed=1, position=(2,0), grid=grid)
    #e4 = Enemie(name='e4', num=1, speed=5, position=(4,1), grid=grid)
    #e5 = Enemie(name='e5', num=1, speed=5, position=(2,1), grid=grid)
    #e6 = Enemie(name='e6', num=1, speed=5, position=(4,1), grid=grid)

    grid.addPlant(p1)
    grid.addPlant(p2)

    grid.addEnemyCluster(e1)
    grid.addEnemyCluster(e2)
    grid.addEnemyCluster(e3)

    sim = Simulation(grid)
    sim.run()

    #gui = Gui()
    #gui.mainloop()