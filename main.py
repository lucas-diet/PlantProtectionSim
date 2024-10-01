
###  bequemlichkeit  ###
import os            ###
os.system('clear')   ###
########################

from models.plant import Plant
from models.enemy import Enemy
from models.enemyCluster import EnemyCluster
from models.grid import Grid

from models.substance import Substance
from models.toxin import Toxin

from controllers.simulation import Simulation

from views.gui import Gui


grid = Grid(height=6, width=6)
plantColor = ['#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']

#name, initEnergy, growthRateEnegry, minEnegrgy, reproduction, offspingEnergy, minDist, maxDist, position, grid
p1 = Plant(name='p1', 
           initEnergy=100, 
           growthRateEnegry=1, 
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
           growthRateEnegry=1,
           minEnegrgy=50, 
           reproductionIntervall=0, 
           offspingEnergy=60, 
           minDist=1,
           maxDist=2, 
           position=(4, 3), 
           grid=grid,
           color = plantColor[1])

p3 = Plant(name='p3', 
           initEnergy=100,
           growthRateEnegry=1,
           minEnegrgy=50, 
           reproductionIntervall=0, 
           offspingEnergy=60, 
           minDist=1,
           maxDist=2, 
           position=(2, 5), 
           grid=grid,
           color = plantColor[1])
    

e1 = Enemy(name='e1', symbol='E1')
e2 = Enemy(name='e2', symbol='E2')
e3 = Enemy(name='e3', symbol='E3')

ec1 = EnemyCluster(enemy=e1, num=2, speed=1, position=(2,0), grid=grid, eatVictory=10)
ec2 = EnemyCluster(enemy=e2, num=2, speed=1, position=(2,0), grid=grid, eatVictory=20)
ec3 = EnemyCluster(enemy=e3, num=1, speed=1, position=(0,4), grid=grid, eatVictory=20)

grid.addPlant(p1)
grid.addPlant(p2)
#grid.addPlant(p3)

grid.addEnemies(ec1)
#grid.addEnemies(ec2)
#grid.addEnemies(ec3)

s1 = Substance(name='s1', type='signal')
s2 = Substance(name='s2', type='toxin')

tox1 = Toxin(substance=s2, 
             plantTransmitter=[p1, p2],
             energyCosts=1,
             triggerCombination=[['e1', 2]],             #TODO: Signal muss noch mit integiert werden.   
             prodTime=2,
             deadly=False,
             eliminationStrength=['e1', 1],
             alarmDist = 3,
            )
    
grid.addToxin(tox1)
    
sim = Simulation(grid)
sim.run(maxGridEnergy=250, maxEnemyNum=2000)

    

#gui = Gui()
#gui.mainloop()