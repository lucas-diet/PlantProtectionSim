
import os
import time
import pickle as pkl

class Simulation():

    def __init__(self, grid):
        self.grid = grid
        self.simLength = 0

    
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


    def noSpecificPlantBreak(self, pName=None):
        if pName is not None:
            # Prüfe, ob es eine Pflanze mit dem angegebenen Namen gibt
            for plant in self.grid.plants:
                if plant.name == pName:
                    return False  # Eine Pflanze mit diesem Namen existiert noch
            print(f'No more plants of type {pName}')
            return True  # Keine Pflanze mit diesem Namen existiert
        else:
            return False  # Kein spezifischer Name angegeben


    
    def noSpeceficEnemyBreak(self, ecName=None):
        if ecName is not None:
            for ec in self.grid.enemies:
                if ec.name == ecName:
                    return False
                print(f'no more enemies of {ec.enemy.name}')
                return True
            else:
                return True
        
    
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
        temp_counts = {}  # Zwischenspeicher für zählbare Pflanzen
        temp_energy = {}  # Zwischenspeicher für Energie

        # Bestimme die maximale Anzahl von Pflanzen, die in das Grid passen
        max_plants = self.grid.width * self.grid.height  # Beispiel: Anzahl der Gridfelder

        # Zählen der Pflanzen pro Typ
        for plant in self.grid.plants:
            if (plant.name, timeStep) not in temp_counts:
                temp_counts[(plant.name, timeStep)] = 0
                temp_energy[(plant.name, timeStep)] = 0
            temp_counts[(plant.name, timeStep)] += 1
            temp_energy[(plant.name, timeStep)] += plant.currEnergy

        # Überprüfen, ob die Anzahl der Pflanzen den maximalen Wert überschreitet
        total_plant_count = sum(temp_counts.values())
        if total_plant_count > max_plants:
            excess_plants = total_plant_count - max_plants
            # Reduziere die Anzahl der Pflanzen (z.B. entferne überschüssige Pflanzen)
            for key in temp_counts:
                # Berechne die überschüssigen Pflanzen und reduziere den Zähler
                temp_counts[key] = max(0, temp_counts[key] - excess_plants)
                excess_plants -= max(0, temp_counts[key])

                # Breche ab, wenn keine überschüssigen Pflanzen mehr zu entfernen sind
                if excess_plants <= 0:
                    break

        # Übertrage die aggregierten Daten in 'plantData'
        for key in temp_counts:
            self.grid.plantData[key] = {'energy': temp_energy[key], 'count': temp_counts[key]}


    def getEnemyData(self, timeStep):
        """_summary_
            Erfasst die Gruppengröße und Anzahl der Feinde pro Typ in einem Dictionary.
        Args:
            timeStep (int): Der aktuelle Zeitschritt der Simulation.
        """
        temp_counts = {}  # Zwischenspeicher für die Anzahl der Gruppen
        temp_sizes = {}   # Zwischenspeicher für die Gruppengröße

        for ec in self.grid.enemies:
            key = (ec.enemy.name, timeStep)
            if key not in temp_counts:
                temp_counts[key] = 0
                temp_sizes[key] = 0
            temp_counts[key] += 1  # Jede 'ec' zählt als eine Gruppe
            temp_sizes[key] += ec.num  # Summe aller Feindgrößen

        # Übertrage die aggregierten Daten in 'EnemyData'
        for key in temp_counts:
            self.grid.EnemyData[key] = {'size': temp_sizes[key], 'count': temp_counts[key]}

    
    def logSafer(self, logArr):
        with open('log.pkl', 'wb') as file:
            pkl.dump(logArr, file)

    
    def logLoader(self, filename):
        with open(filename, 'rb') as file:
            log = pkl.load(file)
        for itm in log:
            print(itm)
  

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
            self.grid.log.append(f'\n##### Simulation-Step: {count} ######\n')
            self.runStep()
            self.grid.collectAndManageEnemies()
            self.grid.removeDeadCluster()
            self.grid.checkAndSplit(count)
            self.grid.displayGridEnergy()
            self.grid.displayEnemyNum()
            self.grid.displayGrid()  
            self.getPlantData(count)
            self.getEnemyData(count)
            
            count += 1
            #time.sleep(1)
        self.simLength = count - 1

            
