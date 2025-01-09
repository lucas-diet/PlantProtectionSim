

import os
os.system('clear')

from models.plant import Plant
from models.enemyCluster import Enemy, EnemyCluster
from models.grid import Grid

from models.connection import SymbioticConnection, AirConnection

from models.substance import Substance
from models.signal import Signal
from models.toxin import Toxin

from controllers.simulation import Simulation

from views.gui import Gui
from views.diagrams import Diagrams

grid = Grid(height=80, width=80)
PLANT_COLORS = ['#00FF00', '#32CD32', '#228B22', '#006400', 
                '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', 
                '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', 
                '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']

# Pflanzen
p1 = Plant(name='p1', initEnergy=100, growthRateEnergy=1, minEnergy=50, 
           reproductionInterval=0, offspringEnergy=60, minDist=1, maxDist=3, position=(5, 5), grid=grid, color=PLANT_COLORS)
p2 = Plant(name='p2', initEnergy=110, growthRateEnergy=2, minEnergy=55, 
           reproductionInterval=4, offspringEnergy=60, minDist=2, maxDist=4, position=(15, 10), grid=grid, color=PLANT_COLORS)
p3 = Plant(name='p3', initEnergy=120, growthRateEnergy=3, minEnergy=60, 
           reproductionInterval=5, offspringEnergy=60, minDist=1, maxDist=3, position=(25, 15), grid=grid, color=PLANT_COLORS)
p4 = Plant(name='p4', initEnergy=130, growthRateEnergy=1, minEnergy=65, 
           reproductionInterval=6, offspringEnergy=60, minDist=2, maxDist=5, position=(35, 20), grid=grid, color=PLANT_COLORS)
p5 = Plant(name='p5', initEnergy=140, growthRateEnergy=2, minEnergy=70, 
           reproductionInterval=7, offspringEnergy=60, minDist=3, maxDist=6, position=(45, 25), grid=grid, color=PLANT_COLORS)
p6 = Plant(name='p6', initEnergy=150, growthRateEnergy=3, minEnergy=75, 
           reproductionInterval=8, offspringEnergy=60, minDist=1, maxDist=3, position=(55, 30), grid=grid, color=PLANT_COLORS)
p7 = Plant(name='p7', initEnergy=160, growthRateEnergy=1, minEnergy=80, 
           reproductionInterval=9, offspringEnergy=60, minDist=2, maxDist=4, position=(65, 35), grid=grid, color=PLANT_COLORS)
p8 = Plant(name='p8', initEnergy=170, growthRateEnergy=2, minEnergy=85, 
           reproductionInterval=10, offspringEnergy=60, minDist=1, maxDist=2, position=(75, 40), grid=grid, color=PLANT_COLORS)

# Feinde
e1 = Enemy(name='e1', symbol='E1')
e2 = Enemy(name='e2', symbol='E2')
e3 = Enemy(name='e3', symbol='E3')
e4 = Enemy(name='e4', symbol='E4')

ec1 = EnemyCluster(enemy=e1, num=3, speed=1, position=(0, 5), grid=grid, eatingSpeed=1, eatVictory=1)
ec2 = EnemyCluster(enemy=e2, num=4, speed=2, position=(0, 10), grid=grid, eatingSpeed=2, eatVictory=2)
ec3 = EnemyCluster(enemy=e3, num=5, speed=1, position=(10, 5), grid=grid, eatingSpeed=1, eatVictory=3)
ec4 = EnemyCluster(enemy=e4, num=6, speed=2, position=(10, 10), grid=grid, eatingSpeed=2, eatVictory=4)

# Substanzen
s1 = Substance(name='s1', type='signal')
s2 = Substance(name='s2', type='signal')
s3 = Substance(name='s3', type='signal')
s4 = Substance(name='s4', type='toxin')
s5 = Substance(name='s5', type='toxin')

sig1 = Signal(substance=s1, emit=[p1, p2], receive=[p1, p2], 
              triggerCombination=[[e1, 2]], prodTime=3, spreadType='symbiotic', 
              sendingSpeed=2, energyCosts=1, afterEffectTime=2)

sig2 = Signal(substance=s2, emit=[p3, p4], receive=[p3, p4], 
              triggerCombination=[[e2, 3]], prodTime=4, spreadType='air', 
              sendingSpeed=3, energyCosts=2, afterEffectTime=3)

tox1 = Toxin(substance=s4, plantTransmitter=[p1, p2], energyCosts=5, 
             triggerCombination=[[sig1, e1, 3]], prodTime=5, deadly=True, 
             eliminationStrength=3)

tox2 = Toxin(substance=s5, plantTransmitter=[p3, p4], energyCosts=4, 
             triggerCombination=[[sig2, e2, 2]], prodTime=4, deadly=False, 
             eliminationStrength=2)

grid.addPlant(p1)
grid.addPlant(p2)
grid.addPlant(p3)
grid.addPlant(p4)
grid.addPlant(p5)
grid.addPlant(p6)
grid.addPlant(p7)
grid.addPlant(p8)

grid.addEnemies(ec1)
grid.addEnemies(ec2)
grid.addEnemies(ec3)
grid.addEnemies(ec4)

grid.addSubstance(sig1)
grid.addSubstance(sig2)
grid.addSubstance(tox1)
grid.addSubstance(tox2)

sc1 = SymbioticConnection(p1, p2)
sc2 = SymbioticConnection(p3, p4)

sc1.createConnection()
sc2.createConnection()





sim = Simulation(grid)
sim.run(maxSteps=20, plant=None, ec=None, maxGridEnergy=None, maxEnemyNum=None)

dia = Diagrams(grid)
#dia.dataPlotter(grid.plantData, sim.simLength, measure='energy', title='Energy by Plant Type Over Time')
#dia.dataPlotter(grid.plantData, sim.simLength, measure='count', title='Number by Plant Types Over Time')
#dia.dataPlotter(grid.EnemyData, sim.simLength, measure='size', title='Clustersize by Enemy Type Over Time')
#dia.dataPlotter(grid.EnemyData, sim.simLength, measure='count', title='Number by Enemy Types Over Time')

# Beinhaltet die DEBUG-Prints, die bei bedarf ausgegen werden können.
#sim.logSafer(grid.log)
#sim.logLoader('log.pkl')

gui = Gui()
gui.mainloop()