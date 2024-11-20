
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
        self.grid = [[(None, []) for _ in range(width)] for _ in range(height)]
        self.totalEnergy = 0


    def getGrid(self):
        return self.grid
    

    def canAddItem(self, min, max, list):
        if len(list) >= min or len(list) <= max:
            return True
        else:
            False

    
    def addPlant(self, plant):
        x,y = plant.position
        if self.canAddItem(1, 16, self.plants) == True:
            self.plants.append(plant)
            _, ecs = self.grid[x][y]
            self.grid[x][y] = (plant, ecs)
        else:
            print('[INFO]: maximale anzahl an pflanzen überschritten/ unterschritten')

    
    def removePlant(self, plant):
        x,y = plant.position
        if plant in self.plants:
            self.plants.remove(plant)
        
        _, ecs = self.grid[x][y]
        self.grid[x][y] = (None, ecs)

    
    def isOccupied(self, position):
        x,y = position
        if self.grid[x][y][0] is None:
            return False
        return True
    

    def isWithinBounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    

    def addEnemies(self, ec):
        x,y = ec.position
        if self.canAddItem(0, 15, self.enemies):
            self.enemies.append(ec)
            plant, ecs = self.grid[x][y]  # Hole das bestehende Tupel
            ecs.append(ec)  # Füge den Feind zur Liste der Feindgruppen hinzu
            self.grid[x][y] = (plant, ecs)  # Speichere das aktualisierte Tupel zurück
        else:
            print('[INFO]: maximale anzahl an fressfeinden überschritten/ unterschritten')


    def removeEnemies(self, ec):
        x,y = ec.position
        if ec in self.enemies:
            self.enemies.remove(ec)
        
        plant, ecs = self.grid[x][y]

        if ec in ecs:
            ecs.remove(ec)
        
        self.grid[x][y] = (plant, ecs)


    def addSubstance(self, substance):
        # Iteriere durch das gesamte Grid
        for _, row in enumerate(self.grid):
            for _, (plant, ec) in enumerate(row):
                # Überprüfen, ob die Substanz ein Signal ist und füge es zu den Signalen hinzu
                substances = self.signals + self.toxins
                if self.canAddItem(0 , 15, substances) == True:
                    if substance.type == 'signal':
                        if substance not in self.signals:
                            self.signals.append(substance)
                    # Überprüfen, ob die Substanz ein Toxin ist und füge sie zu den Toxinen hinzu
                    elif substance.type == 'toxin':
                        if substance not in self.toxins:
                            self.toxins.append(substance)
                else:
                    print('maximale anzhal an substanzen überschritten/ unterschritten')     


    def removeSubstance(self, substance):
        # Iteriere durch das gesamte Grid
        for _, row in enumerate(self.grid):
            for _, (plant, ec) in enumerate(row):
                # Überprüfen, ob die Substanz ein Toxin ist und entferne es aus den Toxinen
                if substance.type == 'toxin':
                    if substance in self.toxins:
                        self.toxins.remove(substance)
                # Überprüfen, ob die Substanz ein Signal ist und entferne es aus den Signalen
                elif substance.type == 'signal':
                    if substance in self.signals:
                        self.signals.remove(substance)


    def getDistance(self, pos1, pos2):
        x1,y1 = pos1
        x2,y2 = pos2
        return abs(x1 - x2) + abs(y1 - y2)
    

    def getGridEnergy(self):
        self.totalEnergy = 0
        for plant in self.plants:
            self.totalEnergy += plant.currEnergy
        return self.totalEnergy
    
    
    def getGridEnemyNum(self):
        enemyNum = 0
        for enemy in self.enemies:
            enemyNum += enemy.num
        return enemyNum
    

    def displayGridEnergy(self):
        print(f'Grid-Energy: {self.getGridEnergy()}')
    

    def displayEnemyNum(self):
        print(f'Enemy-Number: {self.getGridEnemyNum()}')


    def helperGrid(self):
        grid = self.grid
        hGrid = []

        for i in range(len(grid)):  # Iteriere über alle Zeilen
            row = []
            for j in range(len(grid[0])):  # Iteriere über alle Spalten
                plant, ecs = grid[i][j]  # Entpacke das Tupel: plant, feindgruppen
                if plant is not None or ecs:  # Wenn entweder eine Pflanze oder Feinde vorhanden sind
                    plantObj = isinstance(plant, Plant)  # Überprüfe, ob eine Pflanze da ist
                    ecObj = any(isinstance(item, EnemyCluster) for item in ecs)  # Überprüfe, ob Feindgruppen da sind
                    
                    if plantObj and ecObj:
                        row.append('PE')  # Wenn sowohl Pflanze als auch Feindgruppe da sind
                    elif plantObj:
                        row.append('P')  # Nur Pflanze
                    elif ecObj:
                        row.append('E')  # Nur Feindgruppe
                else:
                    row.append('#')  # Leeres Feld

            hGrid.append(row)
        
        return hGrid
    

    def displayGrid(self):
        # Hilfsfunktion, um den Inhalt einer Zelle als mehrzeilige Darstellung zu generieren
        def format_cell(cell):
            lines = []
            plant, ecs = cell  # Entpacke das Tupel in Pflanze und Feindgruppen

            if isinstance(plant, Plant):  # Wenn Pflanze vorhanden
                energy = f'{(plant.currEnergy / plant.initEnergy) * 100:.1f}%'

                if any(plant.signalAlarms.values()) == True:
                    lines.append(f'{energy}!')
                elif any(plant.isSignalSignaling.values()) == True and any(plant.toxinAlarms.values()) == False and any(plant.isToxically.values()) == False:
                    lines.append(f'{energy}>')
                elif any(plant.isSignalSignaling.values()) == True and any(plant.toxinAlarms.values()) == True and any(plant.isToxically.values()) == False:
                    lines.append(f'{energy}+')
                elif any(plant.isSignalSignaling.values()) == True and any(plant.toxinAlarms.values()) == False and any(plant.isToxically.values()) == True:
                    lines.append(f'{energy}*')
                else:
                    lines.append(f'{energy}')

            for ec in ecs:  # Iteriere über alle Feindgruppen
                if isinstance(ec, EnemyCluster):
                    if ec.intoxicated:
                        lines.append(f'{ec.enemy.name}-#{ec.num}*')
                    else:
                        lines.append(f'{ec.enemy.name}-#{ec.num}')

            return lines if lines else ['------']  # Wenn nichts da ist, zeige leeres Feld an

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
                        print(f'{"":<10}', end='  ')  # Leerzeilen auffüllen
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
                _, ecs = cell  # Entpacke das Tupel in Pflanze und Feindgruppen
                if any(isinstance(item, EnemyCluster) for item in ecs):  # Überprüfe nur die Feindgruppen (ecs)
                    return True
        return False

    
    def getNewPosition(self, steps):
        for step in steps:
            x, y = step
            if self.isWithinBounds(x, y):  # Überprüfe, ob die Position innerhalb der Grenzen des Grids liegt
                return (x, y)
        
        return None
    

    def updateEnemyClusterPos(self, ec, oldPos, newPos):
        """Aktualisiert die Position eines Feindes im Grid.
        
        Entfernt den Feind von seiner alten Position und fügt ihn an die neue Position hinzu.
        """
        # Entferne den Feind von der alten Position, falls er dort ist
        _, old_ecs = self.grid[oldPos[0]][oldPos[1]]
        if ec in old_ecs:
            old_ecs.remove(ec)

        # Füge den Feind an der neuen Position hinzu, falls er dort noch nicht existiert
        _, new_ecs = self.grid[newPos[0]][newPos[1]]
        if ec not in new_ecs:
            new_ecs.append(ec)

        # Aktualisiere die Position des Feindes
        ec.position = newPos

    
    def canMove(self, ec):
        # Überprüfe, ob genug Zeitschritte vergangen sind, bis Feind sich bewegen darf
        if ec.stepCounter < ec.speed - 1:
            ec.stepCounter += 1
            return False
        # Setze den Schrittzähler zurück und erlaube die Bewegung
        ec.stepCounter = 0
        return True


    def processEnemyMovement(self, ec, oldPos, path):
        # Bewege den Feind gemäß dem Pfad
        steps = ec.move(path)
        
        if steps is None:
            return oldPos
        
        # Finde die neue Position basierend auf den Schritten
        newPos = self.getNewPosition(steps)
        
        if newPos is not None:
            # Entferne den Feind von der alten Position
            _, old_ecs = self.grid[oldPos[0]][oldPos[1]]
            if ec in old_ecs:
                old_ecs.remove(ec)
            
            # Füge den Feind an der neuen Position hinzu
            _, new_ecs = self.grid[newPos[0]][newPos[1]]
            if ec not in new_ecs:
                new_ecs.append(ec)
            
            # Aktualisiere die Position des Feindes
            ec.position = newPos
            return newPos
        else:
            return oldPos
        
    
    def eatAndReproduce(self, ec, plant):
        self.totalEnergy = self.getGridEnergy()
        ec.eatPlant(ec, plant)
        self.totalEnergy -= plant.currEnergy
        ec.reproduce()


    def plantAlarmAndSignalProd(self, ec, dist, plant):      
        for signal in self.signals:
            for trigger in signal.triggerCombination:
                enemy, minClusterSize = trigger
                # Überprüfen, ob der Feind-Cluster zur Pflanze gehört und die Bedingungen für den Alarm erfüllt sind
                if plant in signal.emit and ec.enemy == enemy and plant.position == ec.targetPlant:
                    if ec.num < minClusterSize and ec.num > 0:
                        print(f'[DEBUG-Signal]: {ec.enemy.name} hat nicht die Mindestanzahl erreicht: {ec.num} < {minClusterSize}')
                        continue
                    else:
                        # Wenn die Pflanze noch nicht alarmiert wurde und das Signal produziert werden soll
                        if plant.isSignalAlarmed(signal) == False and plant.isSignalPresent(signal) == False and dist < 1:
                            plant.enemySignalAlarm(signal)  # Alarmiere die Pflanze
                            signal.signalCosts(plant)  # Reduziere Signal-Kosten
                            print(f'[DEBUG-Signal-{signal.name}]: {plant.name} ist alamiert durch {ec.enemy.name}')
                        # Falls die Pflanze schon alarmiert wurde, aber noch kein Signal produziert
                        elif plant.isSignalAlarmed(signal) == True and plant.isSignalPresent(signal) == False:
                            # Überprüfen, ob die Pflanze genug Zeit hatte, das Signal zu produzieren
                            if plant.getSignalProdCounter(ec, signal) < signal.prodTime:
                                plant.incrementSignalProdCounter(ec, signal)  # Erhöhe den Produktionszähler
                                print(f'[DEBUG-Signal-{signal.name}]: Produktionszähler nach Inkrementierung: {plant.signalProdCounters[ec, signal]}')
                            else:
                                # Wenn der Produktionszähler groß genug ist, produziere das Signal
                                plant.makeSignal(signal)
                                signal.activateSignal()
                                signal.signalCosts(plant)  # Reduziere Signal-Kosten
                                print(f'[DEBUG]: {plant.name} besitzt das Signal {signal.name} durch {ec.enemy.name}')
                        # Nachwirkzeit von Signalstoffen    
                        if ec.lastVisitedPlant is not None and ec.lastVisitedPlant.isSignalPresent(signal) == True:
                            if ec.position != ec.lastVisitedPlant.position:
                                if ec.lastVisitedPlant.afterEffectTime > 0:
                                    ec.lastVisitedPlant.setSignalPresence(signal, True)
                                    ec.lastVisitedPlant.afterEffectTime -= 1
                                else:
                                    ec.lastVisitedPlant.setSignalPresence(signal, False)
                                    signal.deactivateSignal()
                            else:
                                ec.lastVisitedPlant.afterEffectTime = signal.afterEffectTime
                        

    def plantAlarmAndPoisonProd(self, ec, dist, plant):
        # TODO: Was ist wenn verschiedene Giftstoffe durch den gleichen Signalstoff ausgelöst werden?

        for toxin, signal in zip(self.toxins, self.signals):
            for trigger in toxin.triggerCombination:
                triggerSignal, enemy, minClusterSize = trigger
                if plant in toxin.plantTransmitter and triggerSignal == signal and ec.enemy == enemy and plant.position == ec.targetPlant:                
                    if ec.num < minClusterSize and ec.num > 0:
                        print(f'[DEBUG-Gift]: {ec.enemy.name} hat nicht die Mindestanzahl erreicht: {ec.num} < {minClusterSize}')
                        continue  # Springe zur nächsten Iteration, wenn die Mindestanzahl nicht erreicht ist
                    else:
                        # Alarmierung der Pflanze, falls nah genug, genug großes Cluster und Signalstoff vorhanden ist.
                        if plant.isSignalPresent(signal) == True and plant.isToxinAlarmed(toxin) == False and plant.isToxinPresent(toxin) == False and dist < 1:
                            plant.enemyToxinAlarm(toxin)
                            toxin.toxinCosts(plant)
                            print(f'[DEBUG-Gift]: {plant.name} ist alamiert durch {ec.enemy.name}')
                        # Giftproduktion nur wenn Pflanze alarmiert ist, nicht giftig, und Zähler unter Produktionszeit ist
                        elif signal in signal.activeSignals and plant.isToxinAlarmed(toxin) == True and plant.isToxinPresent(toxin) == False:
                            if plant.getToxinProdCounter(ec, toxin) < toxin.prodTime:
                                plant.incrementToxinProdCounter(ec, toxin)
                                print(f'[DEBUG-Gift-{toxin.name}]: Produktionszähler nach Inkrementierung: {plant.toxinProdCounters[ec, toxin]}')
                            else:
                                # Pflanze wird giftig, wenn Produktionszeit erreicht
                                plant.makeToxin(toxin)
                                toxin.toxinCosts(plant)
                                print(f'[DEBUG]: {plant.name} ist jetzt giftig durch {ec.enemy.name}')                      
                        # Giftigkeit zurücksetzen, wenn Feind weg ist
                        if ec.lastVisitedPlant is not None and toxin.deadly == False:
                            # Berechnet Distanz zur vorher besuchten Pflanze. Wenn preDist > 0 und isToxic == True, dann soll isToxic = False und Produktionszähler zurückgesetzt werden.
                            preDist = self.getDistance(ec.position, ec.lastVisitedPlant.position)
                            if preDist == 1 and ec.lastVisitedPlant.isToxinPresent(toxin) == True:
                                ec.lastVisitedPlant.setToxinPresence(toxin, False)
                                ec.lastVisitedPlant.resetToxinProdCounter(ec, toxin)
                                print(f'[DEBUG]: {ec.lastVisitedPlant.name} ist nicht mehr giftig, da der Feind weg ist')

    
    def handleSignalEffects(self, ec, plant):
        # Wenn Gridverbindung existiert, dann wird Signal gesendet (falls Cluster-Trigger aktiv)
        for signal in self.signals:
            # Iteriere durch alle Grid-Verbindungen der Pflanze
            for plants, pos in plant.gridConnections.items():
                sPlant, rPlant = plants
                sPos, rPos = pos

                # Prüfen, ob die Pflanzen in der Verbindung übereinstimmen
                if sPlant == plant and signal.spreadType == 'symbiotic':
                    print(f'[DEBUG]: {sPlant.name}{sPlant.position} ist verbunden mit {rPlant.name}{rPos}')
                    
                    if sPos == ec.position and sPlant.isSignaling == True and rPlant in signal.receive:                        
                        # Überprüfe, ob das Signal gesendet werden kann
                        if plant.getSignalSendCounter(ec, signal, rPlant) < signal.sendingSpeed:
                            plant.incrementSignalSendCounter(ec, signal, rPlant)
                        else:
                            plant.sendSignal(rPlant)
                elif sPlant == plant and signal.spreadType == 'air':
                    #TODO: Senden via Luft!!!
                    pass

    
    def getTriggers(self, toxin):
        triggers = []  # Liste zur Speicherung der Trigger
        for trigger in toxin.triggerCombination:
            signal, enemy, minEcSize = trigger
            triggers.append((signal, enemy, minEcSize))  # Rückgabe der Trigger-Kombinationen als Tupel
        return triggers
    

    def handleToxinEffects(self, ec, plant):
        # Setze die zuletzt besuchte Pflanze des Feindes
        ec.lastVisitedPlant = plant
        
        # Durchlaufe die Toxine, um die Effekte zu prüfen
        for toxin in self.toxins:
            # Hole die Trigger-Kombination für das Toxin
            triggers = self.getTriggers(toxin)
            
            # Durchlaufe jedes Trigger-Tupel und prüfe, ob die Bedingungen zutreffen
            for signal, enemy, minClusterSize in triggers:
                # Wenn das Toxin nicht tödlich ist und die Pflanze toxisch ist
                if toxin.deadly == False and plant.isToxinPresent(toxin) == True:
                    # Versuche, den Feind zu verscheuchen
                    newPath, targetPlant = toxin.displaceEnemies(ec, plant, self.plants)
                    
                    # Wenn der Pfad erfolgreich berechnet wurde und eine neue Position vorhanden ist
                    if newPath and newPath != ec.currentPath:
                        ec.currentPath = newPath  # Setze den neuen Pfad des Feindes
                        ec.targetPlant = targetPlant  # Setze die Zielpflanze des Feindes
                        print(f'[DEBUG]: {ec.enemy.name} wird von {plant.name} verscheucht')
                    
                # Wenn das Toxin tödlich ist und die Pflanze toxisch ist und die Bedingungen erfüllt sind
                elif toxin.deadly == True and plant.isToxinPresent(toxin) == True and plant in toxin.plantTransmitter and ec.num >= minClusterSize:
                    toxin.empoisonEnemies(ec)


    def checkNearbyPlants(self, ec):
        # Gehe jede Zeile im Gitter durch
        for i, row in enumerate(self.grid):
            for j, (plant, _) in enumerate(row):  # Entpacke Tupel: (plant, enemy_clusters)
                if isinstance(plant, Plant):  # Nur Pflanzen betrachten
                    dist = self.getDistance(ec.position, (i, j))  # Berechne die Distanz zur Pflanze
                    self.plantAlarmAndSignalProd(ec, dist, plant)  # Alarm und Signalproduktion prüfen
                    self.plantAlarmAndPoisonProd(ec, dist, plant)  # Alarm und Giftproduktion prüfen
                        
                    if (i, j) == ec.position:  # Wenn der Feind auf der Pflanze steht
                        ec.currentPath = []  # Setze den aktuellen Pfad zurück
                        self.eatAndReproduce(ec, plant)  # Feind frisst und reproduziert sich
                        self.handleSignalEffects(ec, plant)  # Signalwirkungen bearbeiten
                        self.handleToxinEffects(ec, plant)  # Giftwirkungen bearbeiten


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
            for j, (_, ec) in enumerate(row):  # Entpacke Tupel: (plant, enemy_clusters)
                if ec:  # Wenn die Liste der Feind-Cluster nicht leer ist
                    for ec in ec:
                        enemies_to_move.append((ec, (i, j)))

        # Bewege alle gesammelten Feinde
        self.manageEnemyClusters(enemies_to_move)


    def getAllGridConnections(self, plant, *scs):
        connections = {}

        for sc in scs:
            # Stelle sicher, dass es sich um eine SymbioticConnection handelt und die Verbindung aktiv ist
            if sc.connect == True:
                # Prüfe, ob die übergebene Pflanze Teil der Verbindung ist
                if sc.plant1 == plant:
                    connections[((sc.plant1.name, sc.plant2.name), (sc.plant1.position, sc.plant2.position))] = True
                elif sc.plant2 == plant:
                    connections[((sc.plant2.name, sc.plant1.name), (sc.plant2.position, sc.plant1.position))] = True

        for key, pos in connections.items():
            print(f'[DEBUG]: {key[0][0]} auf {key[1][0]} --- {key[0][1]} auf {key[1][1]}')
        return connections


    def fillMatrix(self, type, allSignals, allPlants):
        eMat = np.zeros((len(allPlants), len(allSignals)), dtype=int)

        for i, plant in enumerate(allPlants):  # Iteriere über die Pflanzen
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