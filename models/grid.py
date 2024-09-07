
import numpy as np

from models.plant import Plant
from models.enemy import Enemy

class Grid():

    def __init__(self, heigth, width):
        self.heigth = heigth
        self.width = width
        self.plants = []
        self.enemies = []
        self.grid = np.full((heigth, width), None) 
       
    
    def addPlant(self, plant):
        """_summary_
            Fügt eine Pflanze zur Pflanzenliste und Grid hinzu.
            Die Methode speichert die Pflanze in der Liste 'plants' und platziert sie
            an der durch 'plant.position' bestimmten Position im Gitter 'grid'.
        Args:
            plant: Objekt der Klasse Plant 
        """
        self.plants.append(plant)
        self.grid[plant.position] = plant

    
    def removePlant(self, plant):
        """_summary_
            Entfernt eine Pflanze aus der Pflanzenliste und dem Grid.
            Die Methode löscht die Pflanze aus der Liste 'plants' und setzt die 
            Position im Gitter 'grid', die durch 'plant.position' bestimmt ist, auf 'None'.

        Args:
            plant: Objekt der Klasse Plant 
        """
        self.plants.remove(plant)
        self.grid[plant.position] = None


    def isOccupied(self, position):
        """_summary_
            Überprüft, ob eine bestimmte Position im Grid belegt ist.
            Die Methode gibt 'True' zurück, wenn die angegebene 'position' im Grid belegt ist,
            d. h. wenn dort ein Objekt (z. B. eine Pflanze) vorhanden ist; ansonsten 'False'.

        Args:
            position (Tuple): Ein Tupple (x,y), das aus zwei Zahlen besthet

        Returns:
            _type_: _description_
        """
        return self.grid[position] is not None


    def isWithinBounds(self, x, y):
        """_summary_
            Überprüft, ob die gegebenen Koordinaten (x, y) innerhalb der Gittergrenzen liegen.
            Die Methode gibt 'True' zurück, wenn die x- und y-Koordinaten innerhalb der Höhe ('heigth') 
            und Breite ('width') des Gitters liegen; ansonsten 'False'.

        Args:
            x (int): x-Koordiante
            y (int): y-Koordiante

        Returns:
            _type_: _description_
        """
        return 0 <= x < self.heigth and 0 <= y < self.width
    

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
        """_summary_
            Fügt einen Feind zur Feindesliste und zum Grid hinzu.
            Die Methode speichert den Feind in der Liste 'enemies' und platziert ihn
            an der durch 'enemy.position' bestimmten Position im Grid. Falls an
            dieser Position bereits eine Liste von Feinden vorhanden ist, wird der neue Feind
            zur Liste hinzugefügt; andernfalls wird eine neue Liste erstellt und der Feind wird
            darin gespeichert.

        Args:
            enemy: Objekt vom Typ Enemy
        """
        self.enemies.append(enemy)
        if isinstance(self.grid[enemy.position], list):
            self.grid[enemy.position].append(enemy)
        else:
            self.grid[enemy.position] = [enemy]


    
    def removeEnemy(self, enemy):
        """_summary_
            Entfernt einen Feind aus der Feindesliste und dem Grid.
            Die Methode löscht den Feind aus der Liste 'enemies' und entfernt ihn von der
            Position Grid, die durch 'enemy.position' bestimmt ist. Falls an dieser
            Position eine Liste von Feinden vorhanden ist, wird der Feind daraus entfernt. Wenn
            nach dem Entfernen keine weiteren Feinde an dieser Position verbleiben, wird die
            Position im Gitter auf 'None' gesetzt.
        Args:
            enemy: Objekt vom Typ Enemy
        """
        self.enemies.remove(enemy)
        if isinstance(self.grid[enemy.position], list):
            self.grid[enemy.position].remove(enemy)
            if len(self.grid[enemy.position]) == 0:
                self.grid[enemy.position] = None



    def helperGrid(self):
        """_summary_
            Erzeugt eine textuelle Darstellung des Gitters.
            Die Methode erstellt eine 2D-Liste ('hGrid'), die das Grid in eine leicht verständliche Form umwandelt.
            Jede Position im `hGrid` wird wie folgt dargestellt:
            - 'E', wenn an der Position eine Liste von Feinden vorhanden ist,
            - 'P', wenn eine Pflanze vorhanden ist,
            - '*', wenn die Position leer ist.
            Die Methode gibt die erzeugte 2D-Liste zurück.

        Returns:
            hGrid (Liste): 
        """
        grid = self.grid
        hGrid = []
        
        for i in range(0, len(grid)):
            row = []
            for j in range(0, len(grid[0])):
                if grid[i][j] is not None:
                    if isinstance(grid[i][j], list) and any(isinstance(e, Enemy) for e in grid[i][j]):
                        row.append('E')
                    elif isinstance(grid[i][j], Plant):
                        row.append('P')                
                else:
                    row.append('*')
            hGrid.append(row)
        return hGrid

    

    def displayGrid(self):
        """_summary_
            Gibt das Grid in einem strukturierten Layout aus.
            Die Methode bestimmt zunächst die maximale Anzahl an Feinden, die in einem Feld platziert
            sein können, um das Layout zu gestalten. Dann wird das Gitter zeilenweise durchlaufen und
            auf verschiedenen Ebenen angezeigt. Für jede Zelle im Grid wird Folgendes angezeigt:
            - Feinde werden als 'species-#num' dargestellt, wobei 'species' und 'num' Eigenschaften des Feindes sind.
            - Pflanzen werden auf der ersten Ebene durch den Prozentsatz ihrer aktuellen Energie ('currEnergy' im Vergleich zur Initialenergie 'initEnergy') dargestellt.
            - Leere Zellen werden durch '------' oder Leerzeichen repräsentiert.
            Die Methode sorgt für eine klare und strukturierte Ausgabe, wobei jede Ebene und Zeile korrekt formatiert wird.

        """
        # Bestimme die maximale Anzahl an Feinden in einem Feld für das Layout
        max_enemies_in_cell = max(len(cell) if isinstance(cell, list) else 1 for row in self.grid for cell in row)     
        
        for row in self.grid:
            for level in range(max_enemies_in_cell):
                for cell in row:
                    if isinstance(cell, list):
                        if level < len(cell):
                            enemy = cell[level]
                            print(f'{enemy.species}-#{enemy.num} ', end='  ')
                        else:
                            print(' ' * 8, end=' ')  # Leeren Platz lassen, wenn kein Feind auf dieser Ebene
                    elif isinstance(cell, Plant) and level == 0:
                        # Pflanzen nur auf der ersten Ebene darstellen
                        print(f'{(cell.currEnergy / cell.initEnergy) * 100:.1f}%', end='  ')
                    elif cell is None and level == 0:
                        print('------ ', end=' ')
                    else:
                        print(' ' * 8, end=' ')  # Leeren Platz lassen
                print()  # Neue Zeile nach jeder Ebene
            print()  # Zusätzliche neue Zeile nach jeder Zeile im Grid


    def hasPlants(self):
        """_summary_
            Überprüft, ob sich mindestens eine Pflanze im Grid befindet.
            Die Methode durchsucht das gesamte Grid und gibt 'True' zurück, wenn mindestens eine
            Zelle eine Pflanze ('Plant') enthält. Andernfalls wird 'False' zurückgegeben.

        Returns:
            _type_: _description_
        """
        for row in self.grid:
            for plant in row:
                if isinstance(plant, Plant):
                    return True  # Eine Pflanze gefunden, also gibt es noch Pflanzen
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
        print(f'{enemy.species} moved from {oldPos} to {newPos}\n')

    
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
        """_summary_
            Aktualisiert die Position eines Feindes im Grid.
            Die Methode entfernt den Feind von seiner alten Position im Grid und fügt ihn
            an der neuen Position hinzu. Falls an der alten Position mehrere Feinde vorhanden sind,
            wird der Feind aus der Liste entfernt; ist die Liste nach der Entfernung leer, wird die
            Position auf 'None' gesetzt. An der neuen Position wird der Feind zur Liste hinzugefügt,
            oder es wird eine neue Liste erstellt, falls dort noch keine Feinde vorhanden sind.
            Abschließend wird die Position des Feindes auf die neue Position aktualisiert.

        Args:
            enemy: Objekt der Klasse Enemy
            oldPos: Tupel (x,y) -> alte Position
            newPos: Tupel (x,y) -> neue Position
        """
        # Entferne den Feind von der alten Position
        if isinstance(self.grid[oldPos[0]][oldPos[1]], list):
            self.grid[oldPos[0]][oldPos[1]].remove(enemy)

            if len(self.grid[oldPos[0]][oldPos[1]]) == 0:
                self.grid[oldPos[0]][oldPos[1]] = None
        else:
            self.grid[oldPos[0]][oldPos[1]] = None

        # Füge den Feind zur neuen Position hinzu
        if isinstance(self.grid[newPos[0]][newPos[1]], list):
            self.grid[newPos[0]][newPos[1]].append(enemy)
        else:
            self.grid[newPos[0]][newPos[1]] = [enemy]

        # Aktualisiere die Position des Feindes
        enemy.position = newPos


    def moveEachEnemy(self, moveArr):
        """_summary_
            Bewegt jeden Feind entsprechend den angegebenen Bewegungsanweisungen.
            Die Methode durchläuft das Array 'moveArr', das Paare aus Feind und alter Position enthält.
            Für jeden Feind wird überprüft, ob seine 'stepCounter'-Variable den Wert 'speed - 1' erreicht hat.
            Wenn dies nicht der Fall ist, wird der 'stepCounter' erhöht und die Position bleibt unverändert.
            Andernfalls wird 'stepCounter' zurückgesetzt, und der Feind bewegt sich entsprechend den Schritten, die von 'enemy.move()' zurückgegeben werden.
            Die neue Position wird durch 'getNewPosition' ermittelt. Falls die neue Position gültig ist, wird die Funktion 'updateEnemyPosition' aufgerufen, um den Feind an die neue Position zu verschieben.
            Die Methode gibt die Bewegung des Feindes durch 'displayMove' aus und zeigt das aktualisierte Gitter mit `displayGrid` an.

        Args:
            moveArr (Liste): Array mit Tupel (x,y), die diBwewegungsroute repräsentiert
        """
        # Bewege jeden Feind
        for enemy, oldPos in moveArr:
            if not isinstance(enemy,Enemy):
                continue
            if enemy.stepCounter < enemy.speed - 1:
                enemy.stepCounter += 1
                newPos = oldPos
            else:
                enemy.stepCounter = 0
                steps = enemy.move()
                tmpPos = oldPos

                if steps is None:
                    continue
                
                if self.getNewPosition(steps) is not None:
                    newPos = self.getNewPosition(steps) 
                else:
                    newPos = tmpPos

                if oldPos != newPos:
                    self.updateEnemyPosition(enemy, oldPos, newPos)

            self.displayMove(enemy, oldPos, newPos)
            self.displayGrid()
                

    def collectAndMoveEnemies(self):
        """_summary_
            Sammelt alle Feinde im Gitter und bewegt sie.
            Die Methode erstellt eine Liste 'enemies_to_move', die Paare aus Feinden und deren Positionen enthält.
            Dabei werden alle Feinde aus Zellen, die Listen von Feinden enthalten, sowie einzelne Feinde
            in Zellen durchlaufen. Anschließend wird die Methode 'moveEachEnemy' aufgerufen, um die Feinde
            auf Grundlage der gesammelten Daten zu bewegen.

        """
        # Erstelle eine Liste von Feinden mit ihren Positionen
        enemies_to_move = []

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if isinstance(cell, list):
                    for enemy in cell:
                        enemies_to_move.append((enemy, (i, j)))
                elif isinstance(cell, Enemy):
                    enemies_to_move.append((cell, (i, j)))

        self.moveEachEnemy(enemies_to_move)
                
                                        

                    
                    