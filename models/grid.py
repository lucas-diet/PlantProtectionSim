
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
    

    def addPlant(self, plant):
        x,y = plant.position
        self.plants.append(plant)

        _, ecs = self.grid[x][y]
        self.grid[x][y] = (plant, ecs)

    
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
        self.enemies.append(ec)

        plant, ecs = self.grid[x][y]  # Hole das bestehende Tupel
        ecs.append(ec)  # Füge den Feind zur Liste der Feindgruppen hinzu

        self.grid[x][y] = (plant, ecs)  # Speichere das aktualisierte Tupel zurück


    def removeEnemies(self, ec):
        x,y = ec.position
        if ec in self.enemies:
            self.enemies.remove(ec)
        
        plant, ecs = self.grid[x][y]

        if ec in ecs:
            ecs.remove(ec)
        
        self.grid[x][y] = (plant, ecs)


    def addSubstance(self, substance):
        """Fügt eine Substanz entweder zu den Toxinen oder den Signalen hinzu, abhängig vom Typ der Substanz.
        
        Args:
            substance (Substance): Die Substanz, die hinzugefügt werden soll (entweder ein Toxin oder ein Signal).
        """
        # Iteriere durch das gesamte Grid
        for _, row in enumerate(self.grid):
            for _, (plant, ec) in enumerate(row):
                # Überprüfen, ob die Substanz ein Toxin ist und füge sie zu den Toxinen hinzu
                if substance.type == 'toxin':
                    if substance not in self.toxins:
                        self.toxins.append(substance)
                # Überprüfen, ob die Substanz ein Signal ist und füge es zu den Signalen hinzu
                elif substance.type == 'signal':
                    if substance not in self.signals:
                        self.signals.append(substance)


    def removeSubstance(self, substance):
        """Entfernt eine Substanz entweder aus den Toxinen oder den Signalen, abhängig vom Typ der Substanz.
        
        Args:
            substance (Substance): Die Substanz, die entfernt werden soll (entweder ein Toxin oder ein Signal).
        """
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
                if plant.isAlarmed_signal == True:
                    lines.append(f'{(plant.currEnergy / plant.initEnergy) * 100:.1f}%!')
                elif plant.isSignaling == True and plant.isAlarmed_toxin == False and plant.isToxic == False:
                    lines.append(f'{(plant.currEnergy / plant.initEnergy) * 100:.1f}%>')
                elif plant.isSignaling == True and plant.isAlarmed_toxin == True and plant.isToxic == False:
                    lines.append(f'{(plant.currEnergy / plant.initEnergy) * 100:.1f}%+')
                elif plant.isSignaling == True and plant.isAlarmed_toxin == False and plant.isToxic == True:
                    lines.append(f'{(plant.currEnergy / plant.initEnergy) * 100:.1f}%*')
                else:
                    lines.append(f'{(plant.currEnergy / plant.initEnergy) * 100:.1f}%')

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
        """Bestimmt eine neue Position basierend auf den angegebenen Schritten.
        Die Methode prüft jede Position in der Liste 'steps' und gibt die erste Position zurück,
        die innerhalb der Grid-Grenzen liegt, wie von 'isWithinBounds' überprüft. 
        Wenn keine der angegebenen Positionen gültig ist, wird 'None' zurückgegeben.

        Args:
            steps (list of tuples): Liste der möglichen Schritte, als Tupel von (x, y)-Koordinaten.

        Returns:
            tuple: Die erste gültige Position, die innerhalb der Grid-Grenzen liegt, oder None, wenn keine gültige Position gefunden wurde.
        """
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
        _, old_ecs = self.grid[oldPos[0]][oldPos[1]]  # Holen Sie sich den Feind-Cluster aus der alten Position
        if ec in old_ecs:
            old_ecs.remove(ec)

        # Füge den Feind an der neuen Position hinzu, falls er dort noch nicht existiert
        _, new_ecs = self.grid[newPos[0]][newPos[1]]  # Holen Sie sich den Feind-Cluster aus der neuen Position
        if ec not in new_ecs:
            new_ecs.append(ec)

        # Aktualisiere die Position des Feindes
        ec.position = newPos

    
    def canMove(self, ec):
        # Überprüfe, ob der Feind genug Schritte gemacht hat, um sich zu bewegen
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
                        if plant.isAlarmed_signal == False and plant.isSignaling == False and dist < 1:
                            plant.enemySignalAlarm()  # Alarmiere die Pflanze
                            signal.signalCosts(plant)  # Reduziere Signal-Kosten
                            print(f'[DEBUG-Signal]: {plant.name} ist alamiert durch {ec.enemy.name}')
                        # Falls die Pflanze schon alarmiert wurde, aber noch kein Signal produziert
                        elif plant.isAlarmed_signal == True and plant.isSignaling == False:
                            # Überprüfen, ob die Pflanze genug Zeit hatte, das Signal zu produzieren
                            if plant.getSignalProdCounter(ec, signal) < signal.prodTime - 1:
                                plant.incrementSignalProdCounter(ec, signal)  # Erhöhe den Produktionszähler
                                print(f'[DEBUG-Signal]: Produktionszähler nach Inkrementierung: {plant.signalProdCounters[ec, signal]}')
                            else:
                                # Wenn der Produktionszähler groß genug ist, produziere das Signal
                                plant.makeSignal()
                                signal.activateSignal()
                                signal.signalCosts(plant)  # Reduziere Signal-Kosten
                                print(f'[DEBUG]: {plant.name} besitzt das Signal {signal.name} durch {ec.enemy.name}')

                        # Nachwirkzeit von Signalstoffen    
                        if ec.lastVisitedPlant is not None and ec.lastVisitedPlant.isSignaling == True:
                            if ec.position != ec.lastVisitedPlant.position:
                                if ec.lastVisitedPlant.afterEffectTime > 0:
                                    ec.lastVisitedPlant.isSignaling = True
                                    ec.lastVisitedPlant.afterEffectTime -= 1
                                else:
                                    ec.lastVisitedPlant.isSignaling = False
                            else:
                                ec.lastVisitedPlant.afterEffectTime = signal.afterEffectTime
                        


    def plantAlarmAndPoisonProd(self, ec, dist, plant, signal):
        for toxin in self.toxins:
            for trigger in toxin.triggerCombination:
                triggerSignal, enemy, minClusterSize = trigger
                if plant in toxin.plantTransmitter and triggerSignal == signal and ec.enemy == enemy and plant.position == ec.targetPlant:                
                    if ec.num < minClusterSize and ec.num > 0:
                        print(f'[DEBUG-Gift]: {ec.enemy.name} hat nicht die Mindestanzahl erreicht: {ec.num} < {minClusterSize}')
                        continue  # Springe zur nächsten Iteration, wenn die Mindestanzahl nicht erreicht ist
                    else:
                        # Alarmierung der Pflanze, falls nah genug und Signalstoff vorhanden ist.
                        if plant.isSignaling == True and plant.isAlarmed_toxin == False and plant.isToxic == False and dist < 1:
                            plant.enemyToxinAlarm()
                            toxin.toxinCosts(plant)
                            print(f'[DEBUG-Gift]: {plant.name} ist alamiert durch {ec.enemy.name}')
                        
                        # Giftproduktion nur wenn Pflanze alarmiert ist, nicht giftig, und Zähler unter Produktionszeit ist
                        elif plant.isSignaling == True and plant.isAlarmed_toxin == True and plant.isToxic == False:
                            if plant.getToxinProdCounter(ec, toxin) < toxin.prodTime - 1:
                                plant.incrementToxinProdCounter(ec, toxin)
                                print(f'[DEBUG-Gift]: Produktionszähler nach Inkrementierung: {plant.toxinProdCounters[ec, toxin]}')
                            
                            else:
                                # Pflanze wird giftig, wenn Produktionszeit erreicht
                                plant.makeToxin()
                                toxin.toxinCosts(plant)
                                print(f'[DEBUG]: {plant.name} ist jetzt giftig durch {ec.enemy.name}')                      

                        # Giftigkeit zurücksetzen, wenn Feind weg ist
                        if ec.lastVisitedPlant is not None and toxin.deadly == False:
                            # Berechnet Distanz zur vorher besuchten Pflanze. Wenn preDist > 0 und isToxic == True, dann soll isToxic = False und Produktionszähler zurückgesetzt werden.
                            preDist = self.getDistance(ec.position, ec.lastVisitedPlant.position)
                            if preDist == 1 and ec.lastVisitedPlant.isToxic == True:
                                ec.lastVisitedPlant.isToxic = False
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
            for sig, enemy, minClusterSize in triggers:
                # Wenn das Toxin nicht tödlich ist und die Pflanze toxisch ist
                if toxin.deadly == False and plant.isToxic == True:
                    # Versuche, den Feind zu verscheuchen
                    newPath, targetPlant = toxin.displaceEnemies(ec, plant, self.plants)
                    
                    # Wenn der Pfad erfolgreich berechnet wurde und eine neue Position vorhanden ist
                    if newPath and newPath != ec.currentPath:
                        ec.currentPath = newPath  # Setze den neuen Pfad des Feindes
                        ec.targetPlant = targetPlant  # Setze die Zielpflanze des Feindes
                        print(f'[DEBUG]: {ec.enemy.name} wird von {plant.name} verscheucht.')
                    else:
                        print(f'[DEBUG]: {ec.enemy.name} bleibt an der aktuellen Position.')
                    
                # Wenn das Toxin tödlich ist und die Pflanze toxisch ist und die Bedingungen erfüllt sind
                elif toxin.deadly == True and plant.isToxic == True and plant in toxin.plantTransmitter and ec.num >= minClusterSize:
                    toxin.empoisonEnemies(ec)


    def checkNearbyPlants(self, ec):
        # Gehe jede Zeile im Gitter durch
        for i, row in enumerate(self.grid):
            for j, (plant, _) in enumerate(row):  # Entpacke Tupel: (plant, enemy_clusters)
                if isinstance(plant, Plant):  # Nur Pflanzen betrachten
                    dist = self.getDistance(ec.position, (i, j))  # Berechne die Distanz zur Pflanze
                    self.plantAlarmAndSignalProd(ec, dist, plant)  # Alarm und Signalproduktion prüfen
                    for signal in self.signals:
                        self.plantAlarmAndPoisonProd(ec, dist, plant, signal)  # Alarm und Giftproduktion prüfen
                        
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