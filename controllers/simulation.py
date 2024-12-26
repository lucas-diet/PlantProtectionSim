
import os
import time

class Simulation():

    def __init__(self, grid):
        self.grid = grid

    
    def runStep(self):
        """_summary_
            Führt einen Schritt für jede Pflanze im Grid aus.
            Die Methode durchläuft eine Kopie der Pflanzenliste ('self.grid.plants') und führt für jede Pflanze drei Operationen durch:
            - 'grow()': Lässt die Pflanze wachsen.
            - 'survive()': Überprüft, ob die Pflanze genug Energie hat, um zu überleben, und entfernt sie andernfalls.
            - 'reproduce()': Lässt die Pflanze sich fortpflanzen, wenn die Bedingungen erfüllt sind.

        """
        for plant in self.grid.plants[:]:
            plant.grow()
            plant.survive()
            plant.scatterSeed()


    def displayInit(self):
        """_summary_
            Zeigt den initialen Zustand des Gitters an.
            Die Methode gibt eine Übersicht über das Grid zu Beginn der Simulation aus. Sie zeigt zunächst
            die Gesamtenergie im Gitter und die Anzahl der Feinde an. Anschließend wird das gesamte Gitter
            mit seinen aktuellen Pflanzen und Feinden dargestellt. Die Ausgabe wird durch entsprechende
            Trennlinien visuell strukturiert.
        """
        print('\n##########################')
        print('###### initial grid ######')
        print('##########################\n')
        self.grid.displayGridEnergy()
        self.grid.displayEnemyNum()
        self.getPlantData(0)
        self.getEnemyData(0)
        print()
        self.grid.displayGrid()
        #time.sleep(2)


    def noSpecificPlantBreak(self, plant=None):
        if plant is not None:
            if plant not in self.grid.plants:
                print(f'no more plants of {plant.name}')
                return True
        else:
            return False

    
    def noSpeceficEnemyBreak(self, ec=None):
        if ec is not None:
            if ec not in self.grid.enemies:
                print(f'no more enemies of {ec.enemy.name}')
                return True
        else:
            return False
        
    
    def noEnemiesBreak(self):
        if not self.grid.hasEnemies():
            print('no more enemies')
            return True
        return False
    
    
    def noPlantsBreak(self):
        """_summary_
            Überprüft, ob keine Pflanzen mehr im Grid vorhanden sind, und beendet die Simulation falls erforderlich.
            Die Methode überprüft, ob das Gitter keine Pflanzen mehr enthält, indem 'hasPlants' aufgerufen wird.
            Wenn keine Pflanzen vorhanden sind, wird eine entsprechende Nachricht ausgegeben und 'True' zurückgegeben,
            um anzuzeigen, dass die Simulation beendet werden sollte. Andernfalls wird 'False' zurückgegeben.

        Returns:
            True | False: Wenn keine Pflanzen auf dem Grid vorhande, dann True andernfalls False
        """
        if not self.grid.hasPlants():
            print('no more plants')
            return True
        return False


    def upperGridEnergyBreak(self, maxGridEnergy=None):
        if maxGridEnergy is not None:
            if self.grid.getGridEnergy() > maxGridEnergy:
                print('Upper Border -- Grid-Energy')
                return True
        else:
            return False
    

    def upperEnemyNumBreak(self, maxEnemyNum=None):
        if maxEnemyNum is not None:
            if self.grid.getGridEnemyNum() > maxEnemyNum:
                print('Upper Border -- Enemies')
                return True
        else:
            return False


    def clearConsole(self):
        os.system('clear')


    def getPlantData(self, timeStep):
        """_summary_
            Erfasst die Energie und Anzahl der Pflanzen pro Typ in einem Dictionary.
        Args:
            timeStep (int): Der aktuelle Zeitschritt der Simulation.
        """
        for plant in self.grid.plants:
            if (plant.name, timeStep) not in self.grid.plantData:
                self.grid.plantData[(plant.name, timeStep)] = {'energy': 0, 'count': 0}
            
            self.grid.plantData[(plant.name, timeStep)]['energy'] += plant.currEnergy
            self.grid.plantData[(plant.name, timeStep)]['count'] += 1


    def getEnemyData(self, timeStep):
        """_summary_
            Erfasst die Gruppengröße und Anzahl der Feinde pro Typ in einem Dictionary.
        Args:
            timeStep (int): Der aktuelle Zeitschritt der Simulation.
        """
        for ec in self.grid.enemies:
            if (ec.enemy.name, timeStep) not in self.grid.EnemyData:
                self.grid.EnemyData[(ec.enemy.name, timeStep)] = {'size': 0, 'count': 0}
            
            self.grid.EnemyData[(ec.enemy.name, timeStep)]['size'] += ec.num
            self.grid.EnemyData[(ec.enemy.name, timeStep)]['count'] += 1
  

    def run(self, maxSteps, plant, ec, maxGridEnergy, maxEnemyNum):
        """_summary_
            Führt die Hauptsimulationsschleife aus und aktualisiert den Zustand des Grids in jedem Schritt.
            Die Methode beginnt mit der Anzeige des initialen Zustands des Grids ('initDisplay'). 
            In einer Endlosschleife werden nacheinander folgende Überprüfungen durchgeführt:
            - Ob keine Pflanzen mehr vorhanden sind ('noPlantsBreak'), was die Simulation beendet, wenn zutreffend.
            - Ob die Energiegrenze überschritten wurde ('upperGridEnergyBreak'), was die Simulation beendet, wenn zutreffend.
            - Ob die Anzahl der Feinde die Grenze überschritten hat ('upperEnemyNumBreak'), was die Simulation beendet, wenn zutreffend.

            Falls keine der Beendigungsbedingungen zutrifft, wird 'runStep' aufgerufen, um die Pflanzen zu wachsen, zu überleben und sich fortzupflanzen. Danach werden die aktuellen Energien und die Anzahl der Feinde angezeigt, die Feinde werden gesammelt und bewegt. 
            Die Schleife wiederholt sich, bis eine der Beendigungsbedingungen erfüllt ist. Jeder Schritt wird mit einer Schrittzahl ('count') angezeigt.

        """
        self.displayInit()
        count = 1
    
        while True:
            if count - 1 == maxSteps:
                print('maximum number of steps reached')
                break

            if self.noSpecificPlantBreak(plant):
                break

            if self.noSpeceficEnemyBreak(ec):
                break

            if self.noEnemiesBreak():
                break

            if self.noPlantsBreak():
                break
            
            if self.upperGridEnergyBreak(maxGridEnergy):
                break

            if self.upperEnemyNumBreak(maxEnemyNum):
                break
            
            #self.clearConsole()
            print('\nSimulation-Step:', count)
            self.runStep()
            self.grid.collectAndManageEnemies()
            self.grid.displayGridEnergy()
            self.grid.displayEnemyNum()
            self.grid.displayGrid()
            self.getPlantData(count)
            self.getEnemyData(count)
            count += 1
            #time.sleep(1)

            
