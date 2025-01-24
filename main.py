

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

grid = Grid(height=8, width=8)
PLANT_COLORS = ['#00FF00', '#32CD32', '#228B22', '#006400', 
                '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', 
                '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', 
                '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']

p1 = Plant(name='p1', 
           initEnergy=100, 
           growthRateEnergy=1, 
           minEnergy=50, 
           reproductionInterval=0,
           offspringEnergy=90, 
           minDist=1, 
           maxDist=2,
           position=(5, 2), 
           grid=grid,
           color=PLANT_COLORS)
    
p2 = Plant(name='p2', 
           initEnergy=100,
           growthRateEnergy=2,
           minEnergy=50, 
           reproductionInterval=0,
           offspringEnergy=90, 
           minDist=1,
           maxDist=2, 
           position=(5, 5), 
           grid=grid,
           color=PLANT_COLORS)

p3 = Plant(name='p3', 
           initEnergy=100,
           growthRateEnergy=1,
           minEnergy=50, 
           reproductionInterval=0,
           offspringEnergy=90,
           minDist=1,
           maxDist=2, 
           position=(5, 6), 
           grid=grid,
           color=PLANT_COLORS)

e1 = Enemy(name='e1', symbol='E1')
e2 = Enemy(name='e2', symbol='E2')
e3 = Enemy(name='e3', symbol='E3')

ec1 = EnemyCluster(enemy=e1, num=2, speed=1, position=(0,2), grid=grid, eatingSpeed=1, eatVictory=1)
ec2 = EnemyCluster(enemy=e2, num=2, speed=1, position=(0,2), grid=grid, eatingSpeed=1, eatVictory=1)
ec3 = EnemyCluster(enemy=e3, num=1, speed=1, position=(0,4), grid=grid, eatingSpeed=10, eatVictory=10)

s1 = Substance(name='s1', type='signal')
s2 = Substance(name='s2', type='signal')
s3 = Substance(name='s3', type='toxin')
s4 = Substance(name='s4', type='toxin')

sig1 = Signal(substance=s1,
              emit=['p1'],
              receive=['p1'],
              triggerCombination=[['e1', 2]],
              prodTime=2,
              spreadType='symbiotic',
              sendingSpeed=2,
              energyCosts=3,
              afterEffectTime=10)

sig2 = Signal(substance=s2,
              emit=['p1'],
              receive=['p1', 'p2'],
              triggerCombination=[['e1', 2]],
              prodTime=3, 
              spreadType='air',
              sendingSpeed=3,
              energyCosts=1,
              afterEffectTime=3)

tox1 = Toxin(substance=s3, 
             plantTransmitter=['p1'],
             energyCosts=1,
             triggerCombination=[['s1', 'e1', 1]],   
             prodTime=2,
             deadly=True,
             eliminationStrength=3)

tox2 = Toxin(substance=s4,
             plantTransmitter=['p1'],
             energyCosts=1,
             triggerCombination=[['s2', 'e2', 2]],   
             prodTime=3,
             deadly=False,
             eliminationStrength=1)

grid.addPlant(p1)
grid.addPlant(p2)
grid.addPlant(p3)

grid.addEnemies(ec1)
#grid.addEnemies(ec2)
#grid.addEnemies(ec3)

grid.addSubstance(sig1)
grid.addSubstance(sig2)
#grid.addSubstance(tox1)
grid.addSubstance(tox2)
    

sc1 = SymbioticConnection(p1, p2)
sc2 = SymbioticConnection(p2, p3)

#sc1.createConnection()
sc2.createConnection()


# Simulation
sim = Simulation(grid)
#sim.run(maxSteps=30, plant=None, ec=None, maxGridEnergy=None, maxEnemyNum=None)

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
gui.mainloop()