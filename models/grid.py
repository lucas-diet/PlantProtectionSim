
import numpy as np

from models.plant import Plant
from models.enemy import Enemy


class Grid():

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.plants = []
        self.enemies = []
        self.grid = [[[] for _ in range(width)] for _ in range(height)]


    def getGrid(self):
        return self.grid 
    

    def addPlant(self, plant):
        pos = plant.position

        self.plants.append(plant)
        self.grid[pos[0]][pos[1]].append(plant)

    
    def removePlant(self, plant):
        pos = plant.position

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
        energy = 0
        for plant in self.plants:
            energy += plant.currEnergy
        return energy
    

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

    
    def connectPlants(self, pos1, pos2):
        plant1 = self.grid[pos1]
        plant2 = self.grid[pos2]

        # TODO: Symbiose von zwei Pflanzen


    def addEnemy(self, enemy):
        pos = enemy.position

        self.enemies.append(enemy)
        self.grid[pos[0]][pos[1]].append(enemy)

    
    def removeEnemy(self, enemy):
        pos = enemy.position

        self.enemies.remove(enemy)
        self.grid[pos[0]][pos[1]].remove(enemy)

    
    def helperGrid(self):
        grid = self.grid
        hGrid = []

        for i in range(0, len(grid)):
            row = []
            for j in range(0, len(grid[0])):
                if len(grid[i][j]) > 0:
                    plantObj = any(isinstance(item, Plant) for item in grid[i][j])
                    enemyObj = any(isinstance(item, Enemy) for item in grid[i][j])
                    if plantObj and enemyObj:
                        row.append('PE')
                    elif plantObj:
                        row.append('P')
                    elif enemyObj:
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
                    lines.append(f'{(obj.currEnergy / obj.initEnergy) * 100:.1f}%')
                elif isinstance(obj, Enemy):
                    lines.append(f'{obj.species}-#{obj.num}')
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
                    
    
    def displayMove(self, enemy, oldPos, newPos):
        """_summary_
            Zeigt die Bewegung eines Feindes im Gitter an.
            Die Methode gibt eine Nachricht auf der Konsole aus, die den Namen des Feindes ('species'),
            die alte Position ('oldPos') und die neue Position ('newPos') angibt. 

        Args:
            enemy: Objekt der Klasse Enemy
            oldPos: Tupel (x,y) -> alte Position
            newPos: Tupel (x,y) -> neue Position
        """
        print(f'{enemy.species} moved from {oldPos} to {newPos}')

    
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


    def updateEnemyPosition(self, enemy, oldPos, newPos):
        """Aktualisiert die Position eines Feindes im Grid.
        
        Entfernt den Feind von seiner alten Position und fügt ihn an die neue Position hinzu.
        """
        # Entferne den Feind von der alten Position, falls er dort ist
        if enemy in self.grid[oldPos[0]][oldPos[1]]:
            self.grid[oldPos[0]][oldPos[1]].remove(enemy)

        # Füge den Feind an der neuen Position hinzu
        self.grid[newPos[0]][newPos[1]].append(enemy)

        # Aktualisiere die Position des Feindes
        enemy.position = newPos


    def moveEachEnemy(self, moveArr):
        """Bewegt jeden Feind entsprechend den angegebenen Bewegungsanweisungen.
        
        Die Methode durchläuft das Array 'moveArr', das Paare aus Feind und alter Position enthält.
        Für jeden Feind wird überprüft, ob seine 'stepCounter'-Variable den Wert 'speed - 1' erreicht hat.
        Wenn dies nicht der Fall ist, wird der 'stepCounter' erhöht und die Position bleibt unverändert.
        Andernfalls wird der 'stepCounter' zurückgesetzt, und der Feind bewegt sich entsprechend den Schritten, die von 'enemy.move()' zurückgegeben werden.
        Die neue Position wird durch 'getNewPosition' ermittelt. Falls die neue Position gültig ist, wird die Funktion 'updateEnemyPosition' aufgerufen, um den Feind an die neue Position zu verschieben.
        Die Methode gibt die Bewegung des Feindes durch 'displayMove' aus und zeigt das aktualisierte Gitter mit `displayGrid` an.

        Args:
            moveArr (Liste): Array mit Tupel (x,y), die die Bewegungsroute repräsentieren.
        """
        for enemy, oldPos in moveArr:
            if not isinstance(enemy, Enemy):
                continue
            
            # Überprüfen, ob der Schrittzähler die Geschwindigkeit erreicht hat
            if enemy.stepCounter < enemy.speed - 1:
                enemy.stepCounter += 1
                continue  # Bewege den Feind nicht, da der Schrittzähler noch nicht die Geschwindigkeit erreicht hat
            
            # Reset Schrittzähler und erhalte die nächsten Schritte des Feindes
            enemy.stepCounter = 0
            steps = enemy.move()
            
            if steps is None:
                continue
            
            # Bestimme die neue Position
            newPos = self.getNewPosition(steps)
            if newPos is None:
                newPos = oldPos  # Wenn keine gültige Position gefunden wird, bleibe an der alten Position

            # Aktualisiere die Position des Feindes im Grid
            if oldPos != newPos:
                self.updateEnemyPosition(enemy, oldPos, newPos)
                
            # Zeige die Bewegung des Feindes an und aktualisiere das Grid
            self.displayMove(enemy, oldPos, newPos)

            if oldPos == newPos:                                #TODO: Gesamt-Engerieeinheiten werden noch nicht angepasst, bei entfernen einer Pflanze 
                enemy.eatPlant(enemy, oldPos, newPos)

            self.displayGrid()

            

    
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
                        if isinstance(obj, Enemy):
                            enemies_to_move.append((obj, (i, j)))
                elif isinstance(cell, Enemy):  # Einzelnes Enemy-Objekt in der Zelle
                    enemies_to_move.append((cell, (i, j)))

        # Bewege alle gesammelten Feinde
        self.moveEachEnemy(enemies_to_move)