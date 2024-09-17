
class Simulation:

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
            plant.reproduce()


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
        print()
        self.grid.displayGrid()


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
            print('no more plants. simulation ending.')
            return True
        return False
    

    def upperGridEnergyBreak(self):
        if self.grid.getGridEnergy() > 1000:                #TODO: später umschreiben als Parameter
            print('Upper Border -- Grid-Energy')
            return True
        return False
    

    def upperEnemyNumBreak(self):
        if self.grid.getGridEnemyNum() > 100:                #TODO: später umschreiben als Parameter
            print('Upper Border -- Enemies')
            return True
        return False

    
    def run(self):
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
            if self.noPlantsBreak() == True:
                break
            
            if self.upperGridEnergyBreak() == True:
                break

            if self.upperEnemyNumBreak() == True:
                break
            
 
            self.runStep()
            print('Simulation-Step:', count)
            self.grid.collectAndMoveEnemies()
            self.grid.displayGridEnergy()
            self.grid.displayEnemyNum()
            self.grid.displayGrid()
            count += 1
