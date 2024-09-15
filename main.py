
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
    

    ec1 = EnemyCluster(name='ec1', num=2, speed=3, position=(2,0), grid=grid)
    ec2 = EnemyCluster(name='ec2', num=2, speed=1, position=(0,3), grid=grid)
    ec3 = EnemyCluster(name='ec3', num=1, speed=1, position=(2,0), grid=grid)
    #ec4 = Enemie(name='ec4', num=1, speed=5, position=(4,1), grid=grid)
    #ec5 = Enemie(name='ec5', num=1, speed=5, position=(2,1), grid=grid)
    #ec6 = Enemie(name='ec6', num=1, speed=5, position=(4,1), grid=grid)

    grid.addPlant(p1)
    grid.addPlant(p2)

    grid.addEnemyCluster(ec1)
    grid.addEnemyCluster(ec2)
    grid.addEnemyCluster(ec3)

    sim = Simulation(grid)
    sim.run()

    #gui = Gui()
    #gui.mainloop()