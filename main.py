

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
from controllers.fileManager import Exporter, Importer

from views.gui import Gui
from views.diagrams import Diagrams

grid = Grid(height=10, width=10)
PLANT_COLORS = ['#00FF00', '#32CD32', '#228B22', '#006400', 
                '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', 
                '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', 
                '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']

# Pflanzen
p1 = Plant(name='p1', initEnergy=100, growthRateEnergy=1, minEnergy=50, 
           reproductionInterval=0, offspringEnergy=60, minDist=1, maxDist=3, position=(5, 5), grid=grid, color=PLANT_COLORS)
p2 = Plant(name='p2', initEnergy=110, growthRateEnergy=2, minEnergy=55, 
           reproductionInterval=4, offspringEnergy=60, minDist=2, maxDist=4, position=(1, 1), grid=grid, color=PLANT_COLORS)
p3 = Plant(name='p3', initEnergy=120, growthRateEnergy=3, minEnergy=60, 
           reproductionInterval=5, offspringEnergy=60, minDist=1, maxDist=3, position=(5, 2), grid=grid, color=PLANT_COLORS)

# Feinde
e1 = Enemy(name='e1', symbol='E1')
e2 = Enemy(name='e2', symbol='E2')
e3 = Enemy(name='e3', symbol='E3')

ec1 = EnemyCluster(enemy=e1, num=3, speed=1, position=(0, 5), grid=grid, eatingSpeed=1, eatVictory=1)
ec2 = EnemyCluster(enemy=e2, num=4, speed=2, position=(5, 5), grid=grid, eatingSpeed=2, eatVictory=2)
ec3 = EnemyCluster(enemy=e3, num=5, speed=1, position=(8, 5), grid=grid, eatingSpeed=1, eatVictory=3)

# Substanzen
s1 = Substance(name='signal1', type='signal')
s2 = Substance(name='toxin1', type='toxin')

s1 = Substance(name='signal2', type='signal')
s2 = Substance(name='toxin2', type='toxin')


sig1 = Signal(substance=s1, emit=[p1, p2], receive=[p2], 
              triggerCombination=[[e1, 2]], prodTime=3, spreadType='symbiotic', 
              sendingSpeed=2, energyCosts=1, afterEffectTime=2)

sig2 = Signal(substance=s1, emit=[p1, p2], receive=[p2], 
              triggerCombination=[[e1, 2]], prodTime=3, spreadType='symbiotic', 
              sendingSpeed=2, energyCosts=1, afterEffectTime=2)

tox2 = Toxin(substance=s2, plantTransmitter=[p1, p2], energyCosts=4, 
             triggerCombination=[[sig1, e2, 2]], prodTime=4, deadly=False, 
             eliminationStrength=2)

tox3 = Toxin(substance=s2, plantTransmitter=[p1, p2], energyCosts=4, 
             triggerCombination=[[sig2, e1, 2]], prodTime=4, deadly=False, 
             eliminationStrength=2)

grid.addPlant(p1)
grid.addPlant(p2)
grid.addPlant(p3)

grid.addEnemies(ec1)
grid.addEnemies(ec2)
grid.addEnemies(ec3)


grid.addSubstance(sig1)
grid.addSubstance(sig2)
grid.addSubstance(tox2)
grid.addSubstance(tox3)

sc1 = SymbioticConnection(p1, p2)
sc2 = SymbioticConnection(p3, p2)

sc1.createConnection()
sc2.createConnection()

# Simulation
sim = Simulation(grid)
sim.run(maxSteps=20, plant=None, ec=None, maxGridEnergy=None, maxEnemyNum=None)

# Diagramme ohne GUI
dia = Diagrams(grid)
#dia.dataPlotter(grid.plantData, sim.simLength, measure='energy', title='Energy by Plant Type Over Time')
#dia.dataPlotter(grid.plantData, sim.simLength, measure='count', title='Number by Plant Types Over Time')
#dia.dataPlotter(grid.EnemyData, sim.simLength, measure='size', title='Clustersize by Enemy Type Over Time')
#dia.dataPlotter(grid.EnemyData, sim.simLength, measure='count', title='Number by Enemy Types Over Time')

# Export und Import
#Exporter('test.pkl', grid, dia).save()
#rGrid, rDia = Importer('test.pkl').load()
#rSim = Simulation(rGrid)
#rSim.run(maxSteps=20, plant=None, ec=None, maxGridEnergy=None, maxEnemyNum=None)

#rDia.dataPlotter(rGrid.plantData, rSim.simLength, measure='energy', title='Energy by Plant Type Over Time')
#rDia.dataPlotter(rGrid.plantData, rSim.simLength, measure='count', title='Number by Plant Types Over Time')
#rDia.dataPlotter(rGrid.EnemyData, rSim.simLength, measure='size', title='Clustersize by Enemy Type Over Time')
#rDia.dataPlotter(rGrid.EnemyData, rSim.simLength, measure='count', title='Number by Enemy Types Over Time')

# Beinhaltet die DEBUG-Prints, die bei bedarf ausgegen werden können.
#sim.logSafer(grid.log)
#sim.logLoader('log.pkl')

gui = Gui()
#gui.mainloop()