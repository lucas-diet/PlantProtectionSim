
import random

class Plant():

    def __init__(self, name, initEnergy, growthRateEnegry, minEnegrgy, reproductionIntervall, offspingEnergy, minDist, maxDist, position, grid, color):
        self.name = name
        self.initEnergy = initEnergy
        self.currEnergy = initEnergy
        self.growthRateEnegry = growthRateEnegry
        self.minEnergy = minEnegrgy
        self.reproductionIntervall = reproductionIntervall
        self.offspringEnergy = offspingEnergy
        self.minDist = minDist
        self.maxDist = maxDist
        self.position = position
        self.grid = grid
        self.color = color
        
        self.age = 0
        self.isAlarmed = False
        self.isToxic = False
        self.toxinCounters = {} #dict, wo produktionsCounter für jedes [ec, toxin] gespeichert wird.
        self.gridConnections = {}
        

    def grow(self):
        """_summary_
            Lässt die Pflanze wachsen, indem sie ihre Energie erhöht und ihr Alter steigert.
            Die Methode erhöht die aktuelle Energie ('currEnergy') der Pflanze basierend auf der Wachstumsrate ('growthRateEnegry'),
            die als Prozentsatz angegeben ist. Außerdem wird das Alter der Pflanze ('age') um 1 Jahr erhöht.

        """
        self.currEnergy += self.currEnergy * (self.growthRateEnegry / 100)
        self.age += 1


    def survive(self):
        """_summary_
            Überprüft, ob die Pflanze überleben kann und entfernt sie andernfalls.
            Die Methode vergleicht die aktuelle Energie ('currEnergy') der Pflanze mit einem Minimalwert ('minEnergy').
            Wenn die aktuelle Energie unter dem Minimalwert liegt, wird die Pflanze aus dem Gitter entfernt, indem 'removePlant' aufgerufen wird.

        """
        if self.currEnergy < self.minEnergy:
            self.grid.removePlant(self)
            
        
    def scatterSeed(self):
        """_summary_
            Ermöglicht der Pflanze die Fortpflanzung, wenn die Bedingungen erfüllt sind.
            Die Methode überprüft, ob die Pflanze gemäß ihrer Fortpflanzungszyklen ('reproductionSteps') zur Fortpflanzung bereit ist.
            Falls die Pflanze das Fortpflanzungsalter erreicht hat, erzeugt sie eine zufällige Anzahl von Nachkommen (zwischen 1 und 4).
            Jeder Nachkomme wird an einer neu bestimmten Position ('offspringPosition') im Gitter erstellt und zur Gitterstruktur hinzugefügt.
            Die Energie der Pflanze wird um 10 reduziert, um die Fortpflanzung zu unterstützen.

        """
        if self.reproductionIntervall == 0:
            pass

        elif self.age % self.reproductionIntervall == 0:
            for _ in range(random.randint(1, 4)):       ## Zufall zwischen 1 und 4              # Wie viele Kinder soll es max geben?
                offspringPosition = self.setOffspringPos()
                
                if offspringPosition:
                    energyInput = input('Init-Energy of offspring:')                        # Input() famit Energie für jedes Nachkommen individuell ist
                    offspringEnergy = float(energyInput) if energyInput else 100            # default ist 100 Einheiten
                    offspring = Plant(name=self.name, 
                                      initEnergy=self.offspringEnergy, 
                                      growthRateEnegry=self.growthRateEnegry, 
                                      minEnegrgy=self.minEnergy, 
                                      reproductionIntervall=self.reproductionIntervall, 
                                      offspingEnergy=offspringEnergy,
                                      minDist=self.minDist, 
                                      maxDist=self.maxDist, 
                                      position=offspringPosition, 
                                      grid=self.grid,
                                      color = self.color
                    )
                    self.grid.addPlant(offspring)


    def getDirections(self):
        directions = []
        for dx in range(-self.maxDist, self.maxDist+1):
            for dy in range(-self.maxDist, self.maxDist+1):
                dist = abs(dx) + abs(dy)
                if self.minDist <= dist <= self.maxDist:
                    directions.append((dx, dy))
        
        return directions
    

    def setOffspringPos(self):
        """_summary_
            Bestimmt eine gültige Position für einen Nachkommen innerhalb eines definierten Radius.
            Die Methode erstellt eine Liste aller möglichen Richtungen innerhalb eines Kreises um die aktuelle Position
            mit einer maximalen Distanz ('maxDist') und mischt diese zufällig. Anschließend wird jede Richtung geprüft, um
            eine neue Position zu finden, die innerhalb der Gittergrenzen liegt und nicht bereits besetzt ist.
            Falls eine gültige Position gefunden wird, wird diese zurückgegeben. Andernfalls wird 'None' zurückgegeben.

        Returns:
            tuple[int, int] | None: Die neue Position für den Nachkommen als Koordinatenpaar oder 'None', wenn keine gültige Position gefunden wurde.
        """
        
        directions = self.getDirections()
        random.shuffle(directions)

        for dx, dy in directions:
            newX, newY = self.position[0] + dx, self.position[1] + dy

            if self.grid.isWithinBounds(newX, newY):
                if not self.grid.isOccupied((newX, newY)):
                    print(f'[DEBUG]: {self.name} auf {self.position} erzeugt Nachkommen auf {newX, newY}')
                    return (newX, newY)
                else:
                    print(f'[INFO]: Position {newX, newY} ist belegt. Nachkomme wird nicht erzeugt.')
                    pass
            else:
                print(f'[INFO]: Position {newX, newY} liegt außerhalb der Grenzen.')
                pass
            
        return None


    def getColor(self):
        print(self.color)
        return self.color
    
    
    def enemyAlarm(self):
        self.isAlarmed = True
    

    def makeToxin(self):
        self.isAlarmed = False
        self.isToxic = True

    
    def resetToxinProdCounter(self, ec, toxin):
        self.toxinCounters[ec, toxin] = 0


    def incrementToxinProdCounter(self, ec, toxin):
        key = (ec, toxin)
        if key in self.toxinCounters:
            self.toxinCounters[ec, toxin] += 1
        else:
            self.toxinCounters[ec, toxin] = 1


    def getToxinProdCounter(self, ec, toxin):
        key = (ec, toxin)
        return self.toxinCounters.get(key, 0)
