
import os
os.system('clear')

from models.plant import PlantType, Plant 
from models.enemyCluster import Enemy, EnemyCluster
from models.grid import Grid

from models.symCon import SymbioticConnection
from models.airCon import AirConnection

from models.substance import Substance
from models.signal import Signal
from models.toxin import Toxin

from controllers.simulation import Simulation

from views.gui import Gui


grid = Grid(height=6, width=6)
plantColor = ['#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']

pt1 = PlantType(name='p1', color=plantColor)
pt2 = PlantType(name='p2', color=plantColor)
pt3 = PlantType(name='p3', color=plantColor)

p1 = Plant(plantType=pt1, 
           initEnergy=300, 
           growthRateEnegry=1, 
           minEnegrgy=50, 
           reproductionIntervall=0, 
           offspingEnergy=60, 
           minDist=1, 
           maxDist=2,
           position=(4, 3), 
           grid=grid)
    
p2 = Plant(plantType=pt2, 
           initEnergy=200,
           growthRateEnegry=2,
           minEnegrgy=50, 
           reproductionIntervall=0, 
           offspingEnergy=60, 
           minDist=1,
           maxDist=2, 
           position=(0, 3), 
           grid=grid)

p3 = Plant(plantType=pt3, 
           initEnergy=100,
           growthRateEnegry=1,
           minEnegrgy=50, 
           reproductionIntervall=0, 
           offspingEnergy=60, 
           minDist=1,
           maxDist=2, 
           position=(2, 5), 
           grid=grid)

e1 = Enemy(name='e1', symbol='E1')
e2 = Enemy(name='e2', symbol='E2')
e3 = Enemy(name='e3', symbol='E3')

ec1 = EnemyCluster(enemy=e1, num=2, speed=1, position=(2,0), grid=grid, eatingSpeed=5, eatVictory=10)
ec2 = EnemyCluster(enemy=e2, num=2, speed=1, position=(2,0), grid=grid, eatingSpeed=10, eatVictory=10)
ec3 = EnemyCluster(enemy=e3, num=1, speed=1, position=(0,4), grid=grid, eatingSpeed=10, eatVictory=10)

s1 = Substance(name='s1', type='signal')
s2 = Substance(name='s2', type='signal')
s3 = Substance(name='s3', type='toxin')
s4 = Substance(name='s4', type='toxin')

sig1 = Signal(substance=s1,
              emit=[p1],
              receive=[p3],
              triggerCombination=[[e1, 2]],
              prodTime=2,
              spreadType='symbiotic',
              sendingSpeed=2,
              energyCosts=3,
              afterEffectTime=10,
              spreadSpeed=None)

sig2 = Signal(substance=s2,
              emit=[p1, p2],
              receive=[p3],
              triggerCombination=[[e1, 2]],
              prodTime=1, 
              spreadType='air',
              sendingSpeed=1,
              energyCosts=1,
              afterEffectTime=3,
              spreadSpeed=2)

tox1 = Toxin(substance=s3, 
             plantTransmitter=[p1, p2],
             energyCosts=1,
             triggerCombination=[[sig1, e1, 2]],   
             prodTime=1,
             deadly=False,
             eliminationStrength=1)

tox2 = Toxin(substance=s4, 
             plantTransmitter=[p1, p2],
             energyCosts=1,
             triggerCombination=[[sig2, e1, 2]],   
             prodTime=4,
             deadly=False,
             eliminationStrength=1)

grid.addPlant(p1)
grid.addPlant(p2)
#grid.addPlant(p3)

grid.addEnemies(ec1)
#grid.addEnemies(ec2)
#grid.addEnemies(ec3)

grid.addSubstance(sig1)
grid.addSubstance(sig2)
grid.addSubstance(tox1)
grid.addSubstance(tox2)
    

sc1 = SymbioticConnection(p1, p3)
sc2 = SymbioticConnection(p3, p2)

#sc1.createConnection()
#sc2.createConnection()
#grid.getAllGridConnections(p3, sc1)


#ac = AirConnection(p1)
#p2.airSpreadSignal(ec1, sig1)


sim = Simulation(grid)
sim.run(maxSteps=30, plant=None, ec=None, maxGridEnergy=None, maxEnemyNum=None)

#gui = Gui()
#gui.mainloop()