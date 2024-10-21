
import numpy as np


from models.plant import Plant
from models.enemyCluster import EnemyCluster
from models.symConnection import SymbioticConnection

class Grid():

    def __init__(self, height, width):
        self.height = height
        self.width = width
        
        self.plants = []
        self.enemies = []
        self.signals = []
        self.toxins = []
        self.grid = [[[] for _ in range(width)] for _ in range(height)]
        self.totalEnergy = 0


    def getGrid(self):
        return self.grid 
    

    def addPlant(self, plant):
        pos = plant.position

        self.plants.append(plant)
        self.grid[pos[0]][pos[1]].append(plant)

    
    def removePlant(self, plant):
        pos = plant.position

        self.isAlarmed = False
        self.isToxic = False
        
        self.plants.remove(plant)
        self.grid[pos[0]][pos[1]].remove(plant)

    
    def isOccupied(self, position):
        if len(self.grid[position[0]][position[1]]) == 0:
            return False
        return True
    

    def isWithinBounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    

    def addEnemies(self, ec):
        pos = ec.position

        self.enemies.append(ec)
        self.grid[pos[0]][pos[1]].append(ec)

    
    def removeEnemies(self, ec):
        pos = ec.position

        self.enemies.remove(ec)
        self.grid[pos[0]][pos[1]].remove(ec)


    def addSubstance(self, substance):
        if substance.type == 'toxin':
            self.toxins.append(substance)
        elif substance.type == 'signal':
            self.signals.append(substance)
    
    
    def removeSubstance(self, substance):
        if substance.type == 'toxin':
            self.toxins.remove(substance)
        elif substance.type == 'signal':
            self.signals.remove(substance)


    def getDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    

    def getGridEnergy(self):
        """_summary_
            Berechnet die Gesamtenergie aller Pflanzen im Gitter.
            Die Methode summiert die aktuelle Energie ('currEnergy') jeder Pflanze in der Pflanzenliste 'plants' 
            und gibt die Gesamtsumme als Energiewert zurück.

        Returns:
            energy (int): Summe der vorhanden Energieeinheiten im Netzwerk
        """
        self.totalEnergy = 0
        for plant in self.plants:
            self.totalEnergy += plant.currEnergy
        return self.totalEnergy
    
    
    def getGridEnemyNum(self):
        """_summary_
            Berechnet die Gesamtzahl aller Feinde im Gitter.
            Die Methode summiert die Anzahl ('num') jedes Feindes in der Feindesliste 'enemies' 
            und gibt die Gesamtsumme zurück.

        Returns:
            enemyNum (int): Gesamtzahl aller Feinde im Netzwerk
        """
        enemyNum = 0
        for enemy in self.enemies:
            enemyNum += enemy.num
        return enemyNum
    

    def displayGridEnergy(self):
        """_summary_
            Zeigt die Gesamtenergie des Gitters an.
            Die Methode ruft `getGridEnergy` auf, um die Gesamtenergie aller Pflanzen zu berechnen,
            und gibt diesen Wert in einem formatierten String auf der Konsole aus.

        """
        print(f'Grid-Energy: {self.getGridEnergy()}')
    

    def displayEnemyNum(self):
        """_summary_
            Zeigt die Gesamtzahl der im Gird vorhanden Individuen aller Feinde.
            Die Methode ruft 'getGridEnemyNum' auf, um die Gesamtzahl aller Feinde zu berechnen,
            und gibt diesen Wert in einem formatierten String auf der Konsole aus.

        """
        print(f'Enemy-Number: {self.getGridEnemyNum()}')

    
    def helperGrid(self):
        grid = self.grid
        hGrid = []

        for i in range(0, len(grid)):
            row = []
            for j in range(0, len(grid[0])):
                if len(grid[i][j]) > 0:
                    plantObj = any(isinstance(item, Plant) for item in grid[i][j])
                    ecObj = any(isinstance(item, EnemyCluster) for item in grid[i][j])
                    if plantObj and ecObj:
                        row.append('PE')
                    elif plantObj:
                        row.append('P')
                    elif ecObj:
                        row.append('E')
                else:
                    row.append('#')
            hGrid.append(row)
        return hGrid
    

    def displayGrid(self):
        # Hilfsfunktion, um den Inhalt einer Zelle als mehrzeilige Darstellung zu generieren
        def format_cell(cell):
            lines = []
            for obj in cell:
                if isinstance(obj, Plant):
                    if obj.isAlarmed_toxin == True:
                        lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%+')
                    elif obj.isToxic == True:
                        lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%*')
                    elif obj.isAlarmed_signal == True:
                        lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%!')
                    elif obj.isSignaling == True:
                        lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%^')
                    else:
                        lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%')
                elif isinstance(obj, EnemyCluster):
                    if obj.intoxicated == True:
                        lines.append(f'{obj.enemy.name}-#{obj.num}*')
                    else:
                        lines.append(f'{obj.enemy.name}-#{obj.num}')
            return lines if lines else ['------']  # Leeres Feld

        # Alle Zellen vorbereiten, jede Zelle wird zu einer Liste von Zeilen
        formatted_grid = [list(map(format_cell, row)) for row in self.grid]

        # Bestimme die maximale Anzahl der Zeilen in jeder Spalte, um Zeilen korrekt auszurichten
        max_lines_per_row = [max(len(cell) for cell in row) for row in formatted_grid]

        # Drucke jede Zeile des Gitters
        for row_idx, row in enumerate(formatted_grid):
            for line_idx in range(max_lines_per_row[row_idx]):
                for cell in row:
                    # Wenn die Zelle nicht genügend Zeilen hat, füllen wir mit Leerzeichen auf
                    if line_idx < len(cell):
                        print(f'{cell[line_idx]:<10}', end='  ')  # Links ausgerichtet mit fester Breite
                    else:
                        print(f'{'':<10}', end='  ')  # Leerzeilen auffüllen
                print()  # Neue Zeile nach jeder Zeile im Grid
            print()
        print('#################### \n')
    

    def hasPlants(self):
        for row in self.grid:
            for cell in row:
                if any(isinstance(item, Plant) for item in cell):
                    return True
        return False
    

    def hasEnemies(self):
        for row in self.grid:
            for cell in row:
                if any(isinstance(item, EnemyCluster) for item in cell):
                    return True
        return False
                    
    
    def displayMove(self, ec, oldPos, newPos):
        """_summary_
            Zeigt die Bewegung eines Feindes im Gitter an.
            Die Methode gibt eine Nachricht auf der Konsole aus, die den Namen des Feindes ('species'),
            die alte Position ('oldPos') und die neue Position ('newPos') angibt. 

        Args:
            enemy: Objekt der Klasse Enemy
            oldPos: Tupel (x,y) -> alte Position
            newPos: Tupel (x,y) -> neue Position
        """
        print(f'{ec.enemy.name} moved from {oldPos} to {newPos}')

    
    def getNewPosition(self, steps):
        """_summary_
            Bestimmt eine neue Position basierend auf den angegebenen Schritten.
            Die Methode prüft jede Position in der Liste 'steps' und gibt die erste Position zurück,
            die innerhalb der Grid-Grenzen liegt, wie von 'isWithinBounds' überprüft. 
            Wenn keine der angegebenen Positionen gültig ist, wird 'None' zurückgegeben.

        Args:
            steps (_type_): _description_

        Returns:
            _type_: _description_
        """
        for step in steps:
            newPos = (step[0], step[1])
            if self.isWithinBounds(newPos[0], newPos[1]):
                return newPos
            
        return None


    def updateEnemyClusterPos(self, ec, oldPos, newPos):
        """Aktualisiert die Position eines Feindes im Grid.
        
        Entfernt den Feind von seiner alten Position und fügt ihn an die neue Position hinzu.
        """

        # Entferne den Feind von der alten Position, falls er dort ist
        if ec in self.grid[oldPos[0]][oldPos[1]]:
            self.grid[oldPos[0]][oldPos[1]].remove(ec)

        # Füge den Feind an der neuen Position hinzu, falls er dort noch nicht existiert
        if ec not in self.grid[newPos[0]][newPos[1]]:
            self.grid[newPos[0]][newPos[1]].append(ec)

        # Aktualisiere die Position des Feindes
        ec.position = newPos
    

    def canMove(self, ec):
        if ec.stepCounter < ec.speed - 1:
            ec.stepCounter += 1
            return False
        ec.stepCounter = 0
        return True

    
    def processEnemyMovement(self, ec, oldPos, path):
        steps = ec.move(path)
        
        if steps is None:
            return oldPos
        
        newPos = self.getNewPosition(steps)
        if newPos is not None:
            return newPos
        else:
            return oldPos
        
    
    def eatAndReproduce(self, ec, plant):
        self.totalEnergy = self.getGridEnergy()
        ec.eatPlant(ec, plant)
        self.totalEnergy -= plant.currEnergy
        ec.reproduce()
        

    def getTriggers(self, toxin):
        for trigger in toxin.triggerCombination:
            ecName, minEcSize = trigger
        return ecName, minEcSize
    

    def handleToxinEffects(self, ec, plant):
        ec.lastVisitedPlant = plant # Aktualisiere die zuletzt besuchte Pflanze

        for toxin in self.toxins:
            minEcSize = self.getTriggers(toxin)[1]
            if toxin.deadly == False and plant.isToxic == True:
                ec.currentPath, ec.targetPlant = toxin.displaceEnemies(ec, plant, self.plants)
            elif toxin.deadly == True and plant.isToxic == True and plant in toxin.plantTransmitter and ec.num >= minEcSize:
                toxin.empoisonEnemies(ec)

    
    def plantAlarmAndSignalProd(self, ec, dist, plant):
        # Bis jetzt wird die Pflanze nur alamiert, sodass es zur produktion vom Signalstoff führt.
        #TODO: Was passiert nachdem der Signalstoff vorhanden ist. 
        #   1. Giftproduktion.
        #   2. Gridverbindung -> Nachbar warnen -> wird in der Funktion handleSignalEffects bearbeitet.

        for signal in self.signals:
            for trigger in signal.triggerCombination:
                ecName, minClusterSize = trigger
                if plant in signal.emit and ec.enemy.name == ecName and plant.position == ec.targetPlant:
                    if ec.num < minClusterSize and ec.num > 0:
                        print(f'[DEBUG-Signal]: {ec.enemy.name} hat nicht die Mindestanzahl erreicht: {ec.num} < {minClusterSize}')
                        continue
                    else:
                        if plant.isAlarmed_signal == False and plant.isSignaling == False and dist < 1:
                            plant.enemySignalAlarm()
                            signal.signalCosts(plant)
                            print(f'[DEBUG-Signal]: {plant.name} ist alamiert durch {ec.enemy.name}')
                        elif plant.isAlarmed_signal == True and plant.isSignaling == False:
                            if plant.getSignalProdCounter(ec, signal) < signal.prodTime - 1:
                                plant.incrementSignalProdCounter(ec, signal)
                                print(f'[DEBUG-Signal]: Produktionszähler nach Inkrementierung: {plant.signalProdCounters[ec, signal]}')
                            else:
                                plant.makeSignal()
                                signal.activateSignal()
                                signal.signalCosts(plant)
                                print(f'[DEBUG]: {plant.name} besitzt das Signal {signal.name} durch {ec.enemy.name}')
                        

    def plantAlarmAndPoisonProd(self, ec, dist, plant):
        #TODO: Signalstoff integieren in die Triggerkombination.
        for toxin in self.toxins:
            for trigger in toxin.triggerCombination:
                ecName, minClusterSize = trigger
                if plant in toxin.plantTransmitter and ec.enemy.name == ecName and plant.position == ec.targetPlant:
                    if ec.num < minClusterSize and ec.num > 0:
                        print(f'[DEBUG-Gift]: {ec.enemy.name} hat nicht die Mindestanzahl erreicht: {ec.num} < {minClusterSize}')
                        continue  # Springe zur nächsten Iteration, wenn die Mindestanzahl nicht erreicht ist
                    else:
                        # Alarmierung der Pflanze, falls nah genug
                        if plant.isAlarmed_toxin == False and plant.isToxic == False and dist < 1:
                            plant.enemyToxinAlarm()
                            toxin.toxinCosts(plant)
                            print(f'[DEBUG-Gift]: {plant.name} ist alamiert durch {ec.enemy.name}')
                        
                        # Giftproduktion nur wenn Pflanze alarmiert ist, nicht giftig, und Zähler unter Produktionszeit ist
                        elif plant.isAlarmed_toxin == True and plant.isToxic == False:
                            if plant.getToxinProdCounter(ec, toxin) < toxin.prodTime - 1:
                                plant.incrementToxinProdCounter(ec, toxin)
                                print(f'[DEBUG-Gift]: Produktionszähler nach Inkrementierung: {plant.toxinCounters[ec, toxin]}')
                            else:
                                # Pflanze wird giftig, wenn Produktionszeit erreicht
                                plant.makeToxin()
                                toxin.toxinCosts(plant)
                                print(f'[DEBUG]: {plant.name} ist jetzt giftig durch {ec.enemy.name}')                          

                        # Giftigkeit zurücksetzen, wenn Feind weg ist
                        if ec.lastVisitedPlant is not None and toxin.deadly == False:
                            #Berechnet Dist zur voher besuchten Pflanze. Wenn preDist > 0 und isToxic == True, dann soll isToxic = False und Produktionszähler zurückgesetzt werden.
                            preDist = self.getDistance(ec.position, ec.lastVisitedPlant.position)
                            if preDist == 1 and ec.lastVisitedPlant.isToxic == True:
                                ec.lastVisitedPlant.isToxic = False
                                ec.lastVisitedPlant.resetToxinProdCounter(ec, toxin)
                                print(f'[DEBUG]: {ec.lastVisitedPlant.name} ist nicht mehr giftig, da der Feind weg ist')


    def handleSignalEffects(self, ec, plant):
        # Wenn Gridverbindung existiert, dann wird Signal gesendet (falls cluster Trigger ist).
        # Nach ablauf der sendezeit produziert nachbarpflanze auch Signal.

        # TODO-Frage: Soll nach Ankuft des Signals, das Signal direkt präsent sein oder erst produziert werden und danach erst präsent sein?
        for signal in self.signals:
            for plants, pos in plant.gridConnections.items():
                sPlant = plants[0]
                rPlant = plants[1]
                sPos = pos[0]
                rPos = pos[1]
                if sPlant == plant:
                    print(f'[DEBUG]: {sPlant.name}{sPlant.position} ist verbunden mit {rPlant.name}{rPos}')
                    if sPos == ec.position and sPlant.isSignaling == True and rPlant in signal.receive:
                        print(plant.getSignalSendCounter(ec, signal, rPlant), signal.sendingSpeed)
                        if plant.getSignalSendCounter(ec, signal, rPlant) < signal.sendingSpeed:
                            plant.incrementSignalSendCounter(ec, signal, rPlant) 
                        else:
                            plant.sendSignal(rPlant)
                        

    def checkNearbyPlants(self, ec):
        for plant in self.plants:
            if not isinstance(plant, Plant):
                continue
            
            dist = self.getDistance(ec.position, plant.position)
            self.plantAlarmAndSignalProd(ec, dist, plant)
            self.plantAlarmAndPoisonProd(ec, dist, plant)
            
            
            if plant.position == ec.position:
                ec.currentPath = []
                self.eatAndReproduce(ec, plant)
                self.handleSignalEffects(ec, plant)
                self.handleToxinEffects(ec, plant)

    
    def reduceClusterSize(self, ec):
        for toxin in self.toxins:
            if ec.intoxicated == True:
                toxin.killEnemies(ec)
            

    def manageEnemyClusters(self, moveArr):
        for ec, oldPos in moveArr:
            if not isinstance(ec, EnemyCluster):
                continue

            if not self.canMove(ec):
                continue
            
            path = ec.chooseRandomPlant(ec.position)
            newPos = self.processEnemyMovement(ec, oldPos, path)

            self.updateEnemyClusterPos(ec, oldPos, newPos)
            self.checkNearbyPlants(ec)
            self.reduceClusterSize(ec)
    

    def collectAndManageEnemies(self):
        """Sammelt alle Feinde im Gitter und bewegt sie.

        Die Methode erstellt eine Liste 'enemies_to_move', die Paare aus Feinden und deren Positionen enthält.
        Dabei werden alle Feinde aus Zellen, die Listen von Feinden enthalten, sowie einzelne Feinde
        in Zellen durchlaufen. Anschließend wird die Methode 'moveEachEnemy' aufgerufen, um die Feinde
        auf Grundlage der gesammelten Daten zu bewegen.
        """
        enemies_to_move = []

        # Durchlaufe jede Zelle im Gitter
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if isinstance(cell, list):  # Zelle enthält eine Liste von Objekten
                    for obj in cell:
                        if isinstance(obj, EnemyCluster):
                            enemies_to_move.append((obj, (i, j)))
                elif isinstance(cell, EnemyCluster):  # Einzelnes EnemyCluster-Objekt in der Zelle
                    enemies_to_move.append((cell, (i, j)))

        # Bewege alle gesammelten Feinde
        self.manageEnemyClusters(enemies_to_move)


    def getAllGridConnections(self, plant, *scs):
        connections = {}

        for sc in scs:
            # Stelle sicher, dass es sich um eine SymbioticConnection handelt und die Verbindung aktiv ist
            if sc.connect == True:
                # Prüfe, ob die übergebene Pflanze Teil der Verbindung ist
                if sc.plant1 == plant:
                    connections[(sc.plant1.name,sc.plant2.name)] = sc.plant1.position, sc.plant2.position
                elif sc.plant2 == plant:
                    connections[(sc.plant2.name,sc.plant1.name)] = sc.plant2.position,sc.plant1.position

        for key, pos in connections.items():
            print(f'[DEBUG]: {key[0]} auf {pos[0]} --- {key[1]} auf {pos[1]}')
        return connections
    

    def fillMatrix(self, type, allSignals, allPlants):
        eMat = np.zeros((len(allPlants), len(allSignals)), dtype=int)

        for i , plant in enumerate(allPlants):  # Iteriere über die Pflanzen
            for j, signal in enumerate(allSignals):  # Iteriere über die Signale
                if plant in getattr(signal, type):  # Dynamisch auf 'emit' oder 'receive' zugreifen
                    eMat[i][j] = 1
        return eMat
    

    def createInteractionMatrix(self, allSignals, allPlants):
        for type in ['emit', 'receive']:
            if type == 'emit':
                aMat = self.fillMatrix(type, allSignals, allPlants)
            else:
                bMat = self.fillMatrix(type, allSignals, allPlants)
        return (aMat, bMat)
    
    
    def displayInteractionMatrix(self):
        iMat = self.createInteractionMatrix(self.signals, self.plants)
        for mat, type in zip(iMat, ['A', 'B']):
            print(f'{type} = \n {mat}')
