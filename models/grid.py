
from models.plant import Plant
from models.enemyCluster import EnemyCluster


class Grid():

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.plants = []
        self.enemies = []
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

        self.alarmed = False
        self.isPoisonous = False
        
        self.plants.remove(plant)
        self.grid[pos[0]][pos[1]].remove(plant)

    
    def isOccupied(self, position):
        if len(self.grid[position[0]][position[1]]) == 0:
            return False
        return True
    

    def isWithinBounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    

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
    

    def displayGridEnergy(self):
        """_summary_
            Zeigt die Gesamtenergie des Gitters an.
            Die Methode ruft `getGridEnergy` auf, um die Gesamtenergie aller Pflanzen zu berechnen,
            und gibt diesen Wert in einem formatierten String auf der Konsole aus.

        """
        print(f'Grid-Energy: {self.getGridEnergy()}')
        

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
    

    def displayEnemyNum(self):
        """_summary_
            Zeigt die Gesamtzahl der im Gird vorhanden Individuen aller Feinde.
            Die Methode ruft 'getGridEnemyNum' auf, um die Gesamtzahl aller Feinde zu berechnen,
            und gibt diesen Wert in einem formatierten String auf der Konsole aus.

        """
        print(f'Enemy-Number: {self.getGridEnemyNum()}')


    def addEnemies(self, ec):
        pos = ec.position

        self.enemies.append(ec)
        self.grid[pos[0]][pos[1]].append(ec)

    
    def removeEnemies(self, ec):
        pos = ec.position

        self.enemies.remove(ec)
        self.grid[pos[0]][pos[1]].remove(ec)

    
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
                    if obj.alarmed == True:
                        lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%+')
                    elif obj.isPoisonous == True:
                        lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%*')
                    else:
                        lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%')
                elif isinstance(obj, EnemyCluster):
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
        
    
    def eatAndReproduce(self, ec, oldPos, plant, newPos):
        self.totalEnergy = self.getGridEnergy()
        ec.eatPlant(ec, oldPos, plant, newPos)
        self.totalEnergy -= plant.currEnergy
        ec.reproduce(ec)
        
    
    def handlePlantEnemyInteraction(self, ec, plant):
        for toxin in self.toxins:
            if toxin.deadly == True or (plant not in toxin.plantTransmitter and toxin.deadly == False):
                self.eatAndReproduce(ec, plant.position, plant, ec.position)
            elif toxin.deadly == False and plant.isPoisonous == True:
                ec.currentPath, ec.targetPlant = toxin.displaceEnemies(ec, plant, self.plants)


    def checkNearbyPlants(self, ec):
        for plant in self.plants:
            if not isinstance(plant, Plant):
                continue

            dist = self.getDistance(ec.position, plant.position)
            self.plantAlarmAndPoisonProd(ec, dist, plant)

            if plant.position == ec.position:
                #ec.visitedPlants.add(plant.position)
                self.handlePlantEnemyInteraction(ec, plant)
                ec.currentPath = []

    
    def moveEachEnemyCluster(self, moveArr):
        for ec, oldPos in moveArr:
            if not isinstance(ec, EnemyCluster):
                continue

            if not self.canMove(ec):
                continue
            
            path = ec.chooseRandomPlant(ec.position)
            newPos = self.processEnemyMovement(ec, oldPos, path)

            # Überprüfen, ob der Feind sich tatsächlich bewegt hat
            if newPos != oldPos:
            # Aktualisiere die Feindposition, falls er sich bewegt hat
            
                self.updateEnemyClusterPos(ec, oldPos, newPos)
                self.checkNearbyPlants(ec)  # Führe Interaktionen mit nahegelegenen Pflanzen durch 
            else:
                print('\nNICHT BEWEGT\n')


    def plantAlarmAndPoisonProd(self, ec, dist, plant):
        for toxin in self.toxins:
            # Suche nach der passenden Triggerkombination für den Feind
            for trigger in toxin.triggerCombination:
                ecName, minEcSize = trigger  # Extrahiere den Feindnamen und die Mindestanzahl

                # Prüfen, Pflanze das Gift produziert und o der Feindname in der Trigger-Kombination passt
                if plant in toxin.plantTransmitter and ec.enemy.name == ecName:
                    
                    # Prüfen, ob die Mindestanzahl an 'ec.num' erreicht wurde
                    if ec.num < minEcSize:
                        print(f'[DEBUG]: {ec.enemy.name} hat nicht die Mindestanzahl erreicht: {ec.num} < {minEcSize}')
                        continue  # Springe zur nächsten Iteration, wenn die Mindestanzahl nicht erreicht ist
                    
                    if dist > toxin.alarmDist:
                        plant.alarmed = False
                        plant.isPoisonous = False
                    elif dist <= toxin.alarmDist and plant.alarmed == False and plant.position not in ec.visitedPlants and plant.isPoisonous == False:
                        plant.enemyAlarm()
                        print(f'[DEBUG]: {plant.name} ist alamiert durch {ec.enemy.name}')
                    
                    if plant.alarmed == True:
                        if toxin.prodCounter < toxin.prodTime:
                            toxin.prodCounter += 1
                        elif toxin.prodCounter >= toxin.prodTime:
                            plant.makeToxin()
                            plant.isPoisonous = True
                            toxin.toxinCosts(plant)
                        
                    if ec.position == plant.position:
                        toxin.prodCounter = 0

    
    def addToxin(self, toxin):
        self.toxins.append(toxin)
    
    
    def removeToxin(self, toxin):
        self.toxins.remove(toxin)


    def getDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    

    def collectAndMoveEnemies(self):
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
        self.moveEachEnemyCluster(enemies_to_move)

        