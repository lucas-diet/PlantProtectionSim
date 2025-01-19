
import numpy as np

from models.plant import Plant
from models.enemyCluster import EnemyCluster
from models.connection import SymbioticConnection, AirConnection

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
        self.radiusFields = {}
        self.displaceComps = []
        self.afterDeathComps = []

        self.plantData = {}
        self.EnemyData = {}

        self.plantAtPos = {}

        self.log = []


    def getGrid(self):
        return self.grid

    
    def addPlant(self, plant):
        x,y = plant.position
        self.plantAtPos[plant.position] = plant
        self.plants.append(plant)
        _, ecs = self.grid[x][y]
        self.grid[x][y] = (plant, ecs)

    
    def removePlant(self, plant):
        x,y = plant.position
        if plant in self.plants:
            self.plants.remove(plant)

        if plant.position in self.plants:
            del self.plantAtPos[plant.position]

        _, ecs = self.grid[x][y]
        self.grid[x][y] = (None, ecs)

    
    def isOccupied(self, position):
        x,y = position
        if self.grid[x][y][0] is None:
            return False
        return True
    
    def getPlantAt(self, position):
        return self.plantAtPos.get(position)
    

    def isWithinBounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    

    def addEnemies(self, ec):
        x,y = ec.position
        self.enemies.append(ec)
        plant, ecs = self.grid[x][y]  # Hole das bestehende Tupel
        ecs.append(ec)  # Füge den Feind zur Liste der Feindgruppen hinzu
        self.grid[x][y] = (plant, ecs)  # Speichere das aktualisierte Tupel


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
                if substance.type == 'signal':
                    if substance not in self.signals:
                        self.signals.append(substance)
                # Überprüfen, ob die Substanz ein Toxin ist und füge sie zu den Toxinen hinzu
                elif substance.type == 'toxin':
                    if substance not in self.toxins:
                        self.toxins.append(substance)


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
        """_summary_
            Zeigt das Grid an und formatiert die Darstellung für jede Zelle entsprechend der Belegung.
        """
        def format_cell(cell, position):
            """_summary_
                Formatiert eine einzelne Zelle basierend auf ihrer Position:
                - Wenn die Zelle im Signalradius liegt, benutze 'format_cell_in_radius'.
                - Andernfalls benutze 'format_normal_cell'.
            Args:
                cell (tuple): Ein Tupel (plant, enemy_clusters) aus dem Grid.
                position (tuple): Position der Zelle (x, y).

            Returns:
                list: Eine Liste von Strings, die die visuelle Darstellung der Zelle repräsentieren.
            """
            plant, ecs = cell  # Entpacke das Tupel in Pflanze und Feindgruppen

            # Prüfe, ob die Position in einem Signalradius liegt
            for (cPlant, signal), fields in self.radiusFields.items():
                if position in fields:
                    return format_cell_in_radius(plant, ecs, position)

            # Normale Darstellung, wenn die Position nicht im Radius liegt
            return format_normal_cell(plant, ecs)

        def format_cell_in_radius(plant, ecs, position):
            """_summary_
                Formatiert Zellen, die sich innerhalb des Radius befinden.
                - Markiert Zellen ohne Pflanze oder Feind mit mehreren Zeilen '??????' entsprechend der Anzahl überlappender Radien.
                Args:
                    plant (Plant): Eine Pflanzen-Instanz.
                    ecs (list): Eine Liste von EnemyCluster-Objekten.
                    position (tuple): Die Position der Zelle im Grid.
                Returns:
                    list: Eine Liste von Strings, die die Zelle darstellen.
            """
            # Erstelle eine Liste, die sowohl Pflanze als auch Feind darstellt
            lines = []

            # Wenn eine Pflanze vorhanden ist, füge sie zur Anzeige hinzu
            if isinstance(plant, Plant):
                lines.extend(format_plant(plant))

            # Wenn Feindgruppen vorhanden sind, füge sie zur Anzeige hinzu
            if any(isinstance(ec, EnemyCluster) for ec in ecs):
                lines.extend(format_enemy_clusters(ecs))          

            # Anzahl der Radien, die diese Position überdecken
            overlappingRadii = sum(1 for (p, s), fields in self.radiusFields.items() if position in fields)

            # Wenn keine Pflanze und kein Feind vorhanden ist, füge '??????' entsprechend der Anzahl der Radien hinzu
            if not lines:
                lines.extend(['??????'] * overlappingRadii)

            return lines

        def format_normal_cell(plant, ecs):
            """_summary_
                Formatiert eine normale Zelle (außerhalb des Radius).
            Args:
                lant (Plant): Eine Pflanzen-Instanz.
                ecs (list): Liste der Fressfeindcluster auf dem Feld.
            Returns:
                list: Eine Liste von Strings für die Anzeige.
            """
            lines = []

            # Wenn eine Pflanze vorhanden ist, füge sie zur Anzeige hinzu
            if isinstance(plant, Plant):
                lines.extend(format_plant(plant))

            # Wenn Feindgruppen vorhanden sind, füge sie zur Anzeige hinzu
            for ec in ecs:
                if isinstance(ec, EnemyCluster):
                    lines.extend(format_enemy_cluster(ec))

            return lines if lines else ['------']

        def format_plant(plant):
            """_summary_
                Formatiert die Darstellung einer Pflanze:
                - Zeigt den Energiezustand.
                - Markiert ob eine Pflanze alamiert ist oder Substanz (Signalstoff, Giftstoff) produziert (*, +, >, !).
            Args:
                plant (Plant): Die Pflanzen-Instanz.
            Returns:
                list: Eine Liste mit dem formatierten Energiezustand der Pflanze.
            """
            energy = f'{(plant.currEnergy / plant.initEnergy) * 100:.1f}%'

            if any(plant.isToxically.values()):  # Mindestens ein Giftstoff fertig produziert
                return [f'{energy}*']
            elif any(plant.toxinAlarms.values()):  # Giftstoff in Produktion, aber keiner fertig
                return [f'{energy}+']
            elif any(plant.signalAlarms.values()):  # Signal-Alarm
                if any(plant.isSignalSignaling.values()):  # Signal fertig
                    return [f'{energy}>']
                return [f'{energy}!']
            elif any(plant.isSignalSignaling.values()):  # Signal fertig, keine Alarm-Phase
                return [f'{energy}>']
            else:
                # Keine Alarme oder Gifte
                return [f'{energy}']
            
        def format_enemy_cluster(ec):
            """_summary_
                Formatiert eine einzelnes Fressfeindcluster.
            Args:
                ec (EnemyCluster): Eine Fressfeindcluster-Instanz.

            Returns:
                list: Eine Liste, die die Fressfeindcluster darstellt.
            """
            if ec.intoxicated:
                return [f'{ec.enemy.name}-#{int(ec.num)}*']
            else:
                return [f'{ec.enemy.name}-#{int(ec.num)}']

        def format_enemy_clusters(ecs):
            """_summary_
                Formatiert mehrere Fressfeindcluster auf einem Feld.
            Args:
                ecs (list): Eine Liste von EnemyCluster-Instanzen.
            Returns:
                list: Eine Liste von Strings für die Darstellung.
            """
            lines = []
            for ec in ecs:
                lines.extend(format_enemy_cluster(ec))
            return lines

        def get_max_lines_per_row(formatted_grid):
            """_summary_
                Berechnet die maximale Anzahl von Zeilen pro Spalte.
            Args:
                formatted_grid (list): Das formatierte Grid.
            Returns:
                list: Eine Liste der maximalen Zeilenzahlen für jede Spalte.
            """
            return [max(len(cell) for cell in row) for row in formatted_grid]

        def print_grid(formatted_grid, max_lines_per_row):
            """_summary_
                Druckt das Grid, Zeile für Zeile, mit gleichmäßiger Ausrichtung.
            Args:
                formatted_grid (list): Das formatierte Grid.
                max_lines_per_row (list): Maximale Zeilenanzahl pro Spalte.
            """
            for row_idx, row in enumerate(formatted_grid):
                for line_idx in range(max_lines_per_row[row_idx]):
                    for col_idx, cell in enumerate(row):
                        # Wenn die Zelle nicht genügend Zeilen hat, füllen wir mit Leerzeichen auf
                        if line_idx < len(cell):
                            print(f'{cell[line_idx]:<10}', end='  ')  # Links ausgerichtet mit fester Breite
                        else:
                            print(f'{"":<10}', end='  ')  # Leerzeilen auffüllen
                    print()  # Neue Zeile nach jeder Zeile im Grid
                print()

        # Iteriere über alle Zellen im Grid und erstelle die Darstellung
        formatted_grid = []
        for x, row in enumerate(self.grid):
            formatted_row = []
            for y, cell in enumerate(row):
                formatted_cell = format_cell(cell, (x, y))
                formatted_row.append(formatted_cell)
            formatted_grid.append(formatted_row)

        # Bestimme die maximale Anzahl der Zeilen in jeder Spalte, um Zeilen korrekt auszurichten
        max_lines_per_row = get_max_lines_per_row(formatted_grid)

        # Drucke jede Zeile des Grids
        print_grid(formatted_grid, max_lines_per_row)
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

    
    def collectAndManageEnemies(self):
        """Sammelt alle Feinde im Grid und bewegt sie.

        Die Methode erstellt eine Liste 'enemies_to_move', die Paare aus Feinden und deren Positionen enthält.
        Dabei werden alle Feinde aus Zellen, die Listen von Feinden enthalten, sowie einzelne Feinde
        in Zellen durchlaufen. Anschließend wird die Methode 'moveEachEnemy' aufgerufen, um die Feinde
        auf Grundlage der gesammelten Daten zu bewegen.
        """
        enemies_to_move = []

        # Durchlaufe jede Zelle im Grid
        for i, row in enumerate(self.grid):
            for j, (plant, ecs) in enumerate(row):  # Entpacke Tupel: (plant, enemy_clusters)
                if ecs:  # Wenn die Liste der Feind-Cluster nicht leer ist
                    for ec in ecs:
                        enemies_to_move.append((ec, (i, j)))

        # Bewege alle gesammelten Feinde
        self.manageEnemyClusters(enemies_to_move)

    
    def manageEnemyClusters(self, moveArr):
        for ec, oldPos in moveArr:
            if not isinstance(ec, EnemyCluster):
                continue

            if not self.canMove(ec):
                continue
            
            path = ec.chooseRandomPlant(ec.position)
            newPos = self.processEnemyMovement(ec, oldPos, path)

            self.updateEnemyClusterPos(ec, oldPos, newPos)
            self.processInteractionWithPlant(ec)
            self.reduceClusterSize(ec)
        
        self.processNewPathAfterDisplace()
        self.afterEffectTimeAfterDeath()
            

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

    
    def processInteractionWithPlant(self, ec):
        # Gehe jede Zeile im Grid durch
        for i, row in enumerate(self.grid):
            for j, (plant, _) in enumerate(row):  # Entpacke Tupel: (plant, enemy_clusters)
                if isinstance(plant, Plant):  # Nur Pflanzen betrachten
                    dist = self.getDistance(ec.position, (i, j))  # Berechne die Distanz zur Pflanze
                                        
                    self.plantAlarmAndSignalProd(ec, dist, plant)  # Alarm und Signalproduktion prüfen
                    self.plantAlarmAndPoisonProd(ec, dist, plant)  # Alarm und Giftproduktion prüfen

                    if (i, j) == ec.position:  # Wenn der Feind auf der Pflanze steht
                        ec.currentPath = []  # Setze den aktuellen Pfad zurück
                        self.eatAndReproduce(ec, plant)  # Feind frisst und reproduziert sich
                        
                        self.processSignalEffects(ec, plant)  # Signalwirkungen
                        self.processToxinEffects(ec, plant)  # Giftwirkungen


    def reduceClusterSize(self, ec):
        for toxin in self.toxins:
            if ec.intoxicated:
                toxin.killEnemies(ec)

    
    def processNewPathAfterDisplace(self):
        """
            Verarbeitet den neuen Weg nachdem ein Feindcluster durch ein nicht tötliches Gift vertieben wurde.
        """
        # Zustand: Vertreibung durch Gift
        for toxin, ec, plant, signal in self.displaceComps:
            if not ec.currentPath:          
                # Neuer Pfad durch Giftwirkung
                newPath, targetPlant = toxin.displaceEnemies(ec, plant)
                # Setze den neuen Pfad in 'currentPath'
                ec.currentPath = newPath
                ec.targetPlant = targetPlant
                while ec.currentPath:
                    step = ec.currentPath.pop(0)  # Hole den nächsten Schritt
                    newPos = self.processEnemyMovement(ec, ec.position, [step])
                    self.updateEnemyClusterPos(ec, ec.position, newPos)  # Aktualisiere Position im Grid
            else:
                continue
        # Liste der Vertriebenen leeren
        self.displaceComps = []

    
    def afterEffectTimeAfterDeath(self):
        """
            Verarbeitet die Nachwirkeit von Signalen die durch gestorbene Fressfeinde ausgelöst wurden.
        """
        for toxin, ec, plant, signal in self.afterDeathComps:
            for otherSignal in self.signals:
                if plant.isSignalPresent(otherSignal):
                    self.handleAfterEffectTime(ec, plant, otherSignal)
                else:
                    self.handleAfterEffectTime(ec, plant, signal)
            return
        

    def eatAndReproduce(self, ec, plant):
        self.totalEnergy = self.getGridEnergy()
        ec.eatPlant(ec, plant)
        self.totalEnergy -= plant.currEnergy
        ec.reproduce()

    
    def plantAlarmAndSignalProd(self, ec, dist, plant):
        processed_by_enemy = set()  # Zwischenspeicher für Feind-spezifische Bearbeitung

        for signal in self.signals:
            for trigger in signal.triggerCombination:
                triggerEnemy, minClusterSize = trigger
                if plant.name in signal.emit and ec.enemy.name == triggerEnemy and ec.position == plant.position:
                    # Alarmprozess
                    self.processSignalAlarm(ec, dist, plant, signal, trigger)
                    # Produktionsprozess
                    self.processSignalProduction(ec, plant, signal)

            # Nachwirkzeit verarbeiten
            key = (plant, signal)
            if key not in processed_by_enemy and not ec.intoxicated:
                self.handleAfterEffectTime(ec, plant, signal)
                processed_by_enemy.add(key)


    def processSignalAlarm(self, ec, dist, plant, signal, trigger):
        """
        Verarbeitet den Alarmzustand einer Pflanze.
        """
        triggerEnemy, minClusterSize = trigger
        if ec.num < minClusterSize and ec.num > 0:
            self.log.append(f'{ec.enemy.name}({signal.name}): {ec.num} < {minClusterSize} -> {signal.name} wird nicht ausgelöst')
            print(f'[DEBUG]: {ec.enemy.name}({signal.name}): {ec.num} < {minClusterSize} -> {signal.name} wird nicht ausgelöst')
            return
        if not plant.isSignalAlarmed(signal) and not plant.isSignalPresent(signal) and dist < 1:
            plant.enemySignalAlarm(signal)  # Alarmiere die Pflanze
            signal.signalCosts(plant)  # Reduziere Signal-Kosten
            print(f'[DEBUG]: {plant.name}({signal.name}): ist alamiert durch {ec.enemy.name}')


    def processSignalProduction(self, ec, plant, signal):
        """
        Verarbeitet die Signalproduktion einer Pflanze.
        """
        # Wenn der Signalstoff bereits vorhanden ist, keine Produktion notwendig
        if plant.isSignalPresent(signal):
            return
        
        if plant.isSignalAlarmed(signal) and not plant.isSignalPresent(signal):
            # Überprüfen, ob die Pflanze genug Zeit hatte, das Signal zu produzieren
            if plant.getSignalProdCounter(ec, signal) < signal.prodTime:
                plant.incrementSignalProdCounter(ec, signal)  # Erhöhe den Produktionszähler
                self.log.append(f'Produktionszähler {plant.name}({signal.name}, {ec.enemy.name}): {plant.signalProdCounters[ec, signal]}/{signal.prodTime}')
                print(f'[DEBUG]: Produktionszähler {plant.name}({signal.name}, {ec.enemy.name}): {plant.signalProdCounters[ec, signal]}/{signal.prodTime}')
            else:
                # Wenn der Produktionszähler groß genug ist, produziere das Signal
                plant.makeSignal(signal)
                signal.activateSignal()
                signal.signalCosts(plant)  # Reduziere Signal-Kosten
                self.log.append(f'{plant.name}({signal.name}, {ec.enemy.name}) besitzt das Signal durch {ec.enemy.name}')
                print(f'[DEBUG]: {plant.name}({signal.name}, {ec.enemy.name}) besitzt das Signal durch {ec.enemy.name}')

    
    def handleAfterEffectTime(self, ec, plant, signal):
        """
        Verarbeitet die Nachwirkzeit eines Signals für eine Pflanze.
        """
        # Überprüfen, ob das Signal behandelt werden soll
        if not (plant.name in signal.emit and ec.isPlantInLastVisits(plant) and plant.isSignalPresent(signal)):
            return

        # Holen der aktuellen Nachwirkzeit
        currAfterEffectTime = ec.getAfterEffectTime(plant, signal)

        # Reduziere die Nachwirkzeit, falls sie größer als 0 ist
        for trigger in signal.triggerCombination:
            triggerEnemy, minClusterSize = trigger
            if currAfterEffectTime > 0 and ec.enemy.name == triggerEnemy:
                ec.lastVisitedPlants[(plant, signal)] = currAfterEffectTime - 1
                self.log.append(f'Reduziere Nachwirkzeit für {plant.name}({signal.name}, {ec.enemy.name}): {currAfterEffectTime}/{signal.afterEffectTime}')
                print(f'[DEBUG]: Reduziere Nachwirkzeit für {plant.name}({signal.name}, {ec.enemy.name}): {currAfterEffectTime}/{signal.afterEffectTime}')

                # Wenn der Feind erneut da ist, verlängere die Nachwirkzeit oder setze sie zurück
                if currAfterEffectTime > 0:
                    ec.lastVisitedPlants[(plant, signal)] = signal.afterEffectTime
                    return
                
            # Wenn die Nachwirkzeit abgelaufen ist
            if currAfterEffectTime < 1 and ec.enemy.name == triggerEnemy:
                ec.deleteLastVisits(plant, signal)
                plant.setSignalPresence(signal, False)
                plant.signalProdCounters[(ec, signal)] = 0
                self.log.append(f'Nachwirkzeit abgelaufen: {signal.name} entfernen für {plant.name}')
                print(f'[DEBUG]: Nachwirkzeit abgelaufen: {signal.name} entfernen für {plant.name}')

                # Zusätzliche Aktionen basierend auf dem Signaltyp
                if signal.spreadType == 'symbiotic':
                    pass
                elif signal.spreadType == 'air':
                    # Setzte den entstandenen Radius zurück
                    self.removeSignalRadius(plant, signal)
                    return

    
    def plantAlarmAndPoisonProd(self, ec, dist, plant):
        for toxin in self.toxins:
            for signal in self.signals:
                for trigger in toxin.triggerCombination:
                    triggerSignal, triggerEnemy, minClusterSize = trigger
                    
                    if plant.name in toxin.plantTransmitter and signal.name == triggerSignal and ec.enemy.name == triggerEnemy and ec.position == plant.position:
                        # Alarmprozess
                        self.processToxinAlarm(ec, dist, plant, signal, toxin, trigger)
                        # Produktionsprozess
                        self.processToxinProduction(ec, plant, toxin)
 
            self.resetToxically(ec, toxin, plant)


    def processToxinAlarm(self, ec, dist, plant, signal, toxin, trigger):

        triggerSignal, triggerEnemy, minClusterSize = trigger

        if ec.num < minClusterSize and ec.num > 0:
            self.log.append(f'{ec.enemy.name}({toxin.name}): {ec.num} < {minClusterSize} --> {toxin.name} wird nicht ausgelöst')
            print(f'[DEBUG]: {ec.enemy.name}({toxin.name}): {ec.num} < {minClusterSize} --> {toxin.name} wird nicht ausgelöst')
            return
        if plant.isSignalPresent(signal) and not plant.isToxinAlarmed(toxin) and not plant.isToxinPresent(toxin) and dist < 1:
            plant.enemyToxinAlarm(toxin)
            toxin.toxinCosts(plant)

    
    def processToxinProduction(self, ec, plant, toxin):
        """
        Verarbeitet die Giftproduktion einer Pflanze.
        """
        if plant.isToxinAlarmed(toxin) and not plant.isToxinPresent(toxin):
            # Überprüfen, ob die Pflanze genug Zeit hatte, das Gift zu produzieren
            if plant.getToxinProdCounter(ec, toxin) < toxin.prodTime:
                plant.incrementToxinProdCounter(ec, toxin)  # Erhöhe den Produktionszähler
                self.log.append(f'Produktionszähler {plant.name}({toxin.name}, {ec.enemy.name}): {plant.toxinProdCounters[ec, toxin]}/{toxin.prodTime}')
                print(f'[DEBUG]: Produktionszähler {plant.name}({toxin.name}, {ec.enemy.name}): {plant.toxinProdCounters[ec, toxin]}/{toxin.prodTime}')
                # Wenn der Produktionszähler groß genug ist, produziere das Gift
            else:
                plant.makeToxin(toxin)
                toxin.toxinCosts(plant)  # Reduziere Gift-Kosten
                self.log.append(f'{plant.name}({toxin.name}, {ec.enemy.name}) ist jetzt giftig durch {ec.enemy.name}')
                print(f'[DEBUG]: {plant.name}({toxin.name}, {ec.enemy.name}) ist jetzt giftig durch {ec.enemy.name}')
                

    def processSignalEffects(self, ec, plant):
        for signal in self.signals:
            for trigger in signal.triggerCombination:
                triggerEnemy, minClusterSize = trigger
                if triggerEnemy == ec.enemy.name:
                    self.symCommunication(ec, plant, signal)
                    self.airCommunication(ec, plant, signal)
                if plant.currEnergy <= plant.minEnergy:
                    self.removeSignalRadius(plant, signal)


    def processToxinEffects(self, ec, plant):
        """
        Verarbeitet die Effekte von Toxinen auf einen Feind und dessen Interaktion mit einer Pflanze.
        """ 
        for toxin in self.toxins:
            for signal in self.signals:
                for trigger in toxin.triggerCombination:
                    triggerSignal, triggerEnemy, minClusterSize = trigger

                    # Verarbeite nicht-tödliche Toxine
                    if not toxin.deadly and plant.isToxinPresent(toxin) and ec.enemy.name == triggerEnemy and signal.name == triggerSignal and plant.name in toxin.plantTransmitter:
                        self.processNonDeadlyToxin(toxin, ec, plant, signal)
                        self.log.append(f'Nicht-tödliches Toxin ({toxin.name}) verarbeitet für {ec.enemy.name}')
                        print(f'[DEBUG]: Nicht-tödliches Toxin ({toxin.name}) verarbeitet für {ec.enemy.name}')

                    # Verarbeite tödliche Toxine
                    elif toxin.deadly and plant.isToxinPresent(toxin) and plant.name in toxin.plantTransmitter:
                        self.processDeadlyToxin(toxin, ec, plant, signal)
                        print(f'[DEBUG]: Tödliches Toxin ({toxin.name}) verarbeitet für {ec.enemy.name}')


    def processNonDeadlyToxin(self, toxin, ec, plant, signal):
        """
        Speichert (leitet Verarbeitung ein) die Effekte nicht-tödlicher Toxine.
        """
        # Füge die Pflanze zu den letzten Besuchen des Feindes hinzu
        ec.insertLastVisits(plant, signal)
        self.displaceComps.append((toxin, ec, plant, signal))


    def processDeadlyToxin(self, toxin, ec, plant, signal):
        """
        Verarbeitet die Effekte tödlicher Toxine, einschließlich Feind-Vergiftung.
        """
        # Wende den Effekt des tödlichen Toxins auf den Feind an wenn er in dem Trigger vorhanden ist.
        for trigger in toxin.triggerCombination:
            triggerSignal, triggerEnemy, minClusterSize = trigger
            if triggerEnemy == ec.enemy.name and triggerSignal == signal.name:
                toxin.empoisonEnemies(ec)
                self.log.append(f'{ec.enemy.name} wurde durch {toxin.name} vergiftet\n')
                print(f'[DEBUG]: {ec.enemy.name} wurde durch {toxin.name} vergiftet')

                ec.insertLastVisits(plant, signal)
                self.afterDeathComps.append((toxin, ec, plant, signal))
            

    def resetToxically(self, ec, toxin, plant):
        """
        Setzt den Zustand der Pflanze zurück, falls sie nicht mehr toxisch sein sollte.
        """
        if ec.isPlantInLastVisits(plant):
            preDist = self.getDistance(ec.position, plant.position)
            if not toxin.deadly:
                if preDist > 0:
                    plant.setToxinPresence(toxin, False)
                    plant.resetToxinProdCounter(ec, toxin)
        
        if toxin.deadly and plant.isToxinPresent(toxin) and toxin.eliminationStrength >= ec.num:
            plant.setToxinPresence(toxin, False)
            plant.resetToxinProdCounter(ec, toxin)


    def symCommunication(self, ec, plant, signal):
        if plant.name in signal.emit and signal.spreadType == 'symbiotic':
            for plants, plantsPos in plant.gridConnections.items():
                sPlant, rPlant = plants
                sPos, rPos = plantsPos
                
                if rPlant.isSignalPresent(signal):
                    for con in rPlant.gridConnections:
                        next_sPlant, next_rPlant = con[0], con[1]
                        if len(rPlant.gridConnections) > 1 and (next_sPlant, next_rPlant) != (rPlant, sPlant):
                            self.symInteraction(next_sPlant, next_rPlant, signal, ec)
                else:
                    if sPlant.name == plant.name and sPlant.isSignalPresent(signal):
                        self.symInteraction(sPlant, rPlant, signal, ec)
                

    def symInteraction(self, sPlant, rPlant, signal, ec):
        if rPlant.name in signal.receive:
            if sPlant.getSignalSendCounter(ec, signal, rPlant) < signal.sendingSpeed:
                if not rPlant.isSignalPresent(signal):
                    self.log.append(f'{sPlant.name}{sPlant.position} ist verbunden mit {rPlant.name}{rPlant.position}\n')
                    print(f'[DEBUG]: {sPlant.name}{sPlant.position} ist verbunden mit {rPlant.name}{rPlant.position}')
                sPlant.incrementSignalSendCounter(ec, signal, rPlant)
                self.log.append(f'Sendenstatus {signal.name} (Verbindung): {sPlant.name}{sPlant.position} -> {rPlant.name}{rPlant.position}: {sPlant.getSignalSendCounter(ec, signal, rPlant)}/{signal.sendingSpeed}')
                print(f'[DEBUG]: Sendenstatus {signal.name} (Verbindung): {sPlant.name}{sPlant.position} -> {rPlant.name}{rPlant.position}: {sPlant.getSignalSendCounter(ec, signal, rPlant)}/{signal.sendingSpeed}')
            else:
                sPlant.sendSignal(rPlant, signal)
                # Um Rückkopplungen zu vermeiden wird der Counter erst zurückgesetzt wenn die empfangende Pflanze stirbt oder der Sender kein Signalstoff mehr hat.
                if rPlant.currEnergy <= rPlant.minEnergy or not sPlant.isSignalPresent(signal):
                    sPlant.resetSignalSendCounter(ec, signal, rPlant)
                if not rPlant.isSignalPresent(signal):
                    self.log.append(f'Signal gesendet via Symbiose von {sPlant.name}{sPlant.position} zu {rPlant.name}{rPlant.position}')
                    print(f'[DEBUG]: Signal gesendet via Symbiose von {sPlant.name}{sPlant.position} zu {rPlant.name}{rPlant.position}')
        else:
            self.log.append(f'{sPlant.name} und {rPlant.name} sind verbunden. {rPlant.name} kann {signal.name} nicht empfangen.')
            print(f'[DEBUG]: {sPlant.name} und {rPlant.name} sind verbunden. {rPlant.name} kann {signal.name} nicht empfangen.')
            pass 


    def airCommunication(self, ec, plant, signal):
        if plant.name in signal.emit and signal.spreadType == 'air':
            if plant.isSignalPresent(signal):
                # Berechnung der Signalreichweite
                radius = plant.airSignalRange(signal)
                self.log.append(f'Signalreichweite {signal.name}: {radius}')
                print(f'[DEBUG]: Signalreichweite {signal.name}: {radius}')
                self.radiusFields[(plant, signal)] = self.getFieldsInAirRadius(plant, radius)
                self.log.append(f'Streustatus von {signal.name} für {plant.name} gegen {ec.enemy.name}: {plant.getSignalAirSpreadCounter(ec, signal) + 1}/{signal.sendingSpeed}')
                print(f'[DEBUG]: Streustatus von {signal.name} für {plant.name} gegen {ec.enemy.name}: {plant.getSignalAirSpreadCounter(ec, signal) + 1}/{signal.sendingSpeed}')
                
                if plant.getSignalAirSpreadCounter(ec, signal) < signal.sendingSpeed - 1:
                    plant.incrementSignalRadius(ec, signal)
                    signal.signalCosts(plant)  # Reduziere die Signal-Kosten   
                else:
                    self.processSignalRadiusSize(ec, plant, signal) 
    
                self.airInteraction(plant, signal, ec)

  
    def removeSignalRadius(self, plant, signal):
        # Entferne alle Radien und Signale der Pflanze
        keys_to_remove = [(p, s) for (p, s) in self.radiusFields.keys() if p == plant and s == signal]
        for key in keys_to_remove:
            del self.radiusFields[key]
        return  # Abbruch, da Pflanze tot ist


    def getFieldsInAirRadius(self, plant, radius):
        x0, y0 = plant.position
        radiusFields = []

        # Iteriere durch die gesamte Grid-Matrix
        for x in range(len(self.grid)):
            for y in range(len(self.grid[0])):
                dist = np.floor(np.sqrt((x - x0) ** 2 + (y - y0) ** 2))
                if dist <= radius:
                    radiusFields.append((x, y))

        return radiusFields
    

    def processSignalRadiusSize(self, ec, plant, signal):
        # Wenn die Nachwirkzeit nicht abgelaufen ist, erweitere Radius
        plant.resetSignalAirSpreadCounter(ec, signal)
        signal.radius[(plant, signal)] += 1
                
    
    def airInteraction(self, plant, signal, ec):
        for otherPlant in self.plants:
            if otherPlant.name != plant.name and otherPlant.position in self.radiusFields[(plant, signal)] and otherPlant in signal.receive:
                sPlant, rPlant = plant, otherPlant
                sPos, rPos = plant.position, otherPlant.position
                if sPlant.getSignalSendCounter(ec, signal, rPlant) < signal.sendingSpeed:
                    sPlant.incrementSignalSendCounter(ec, signal, rPlant)
                    self.log.append(f'Sendenstatus (Luft): {sPlant.name}{sPlant.position} -> {rPlant.name}{rPlant.position}: {sPlant.getSignalSendCounter(ec, signal, rPlant)}/{signal.sendingSpeed}')
                    print(f'[DEBUG]: Sendenstatus (Luft): {sPlant.name}{sPlant.position} -> {rPlant.name}{rPlant.position}: {sPlant.getSignalSendCounter(ec, signal, rPlant)}/{signal.sendingSpeed}')
                else:
                    sPlant.sendSignal(rPlant, signal)
                    self.log.append(f'Signal gesendet via Luft von {sPlant.name}{sPlant.position} zu {rPlant.name}{rPlant.position}')
                    print(f'[DEBUG]: Signal gesendet via Luft von {sPlant.name}{sPlant.position} zu {rPlant.name}{rPlant.position}')  





    def getAllGridConnections(self, plant, *scs):
        connections = {}

        for sc in scs:
            # Stelle sicher, dass es sich um eine SymbioticConnection handelt und die Verbindung aktiv ist
            if sc.connect:
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