
import random

class Plant():

    def __init__(self, species, initEnergy, growthRateEnegry, minEnegrgy, reproductionSteps, offspingEnergy, minDist, maxDist, position, grid):
        self.species = species
        self.initEnergy = initEnergy
        self.currEnergy = initEnergy
        self.growthRateEnegry = growthRateEnegry
        self.minEnergy = minEnegrgy
        self.reproductionSteps = reproductionSteps
        self.offspringEnergy = offspingEnergy
        self.minDist = minDist
        self.maxDist = maxDist
        self.position = position
        self.grid = grid
        self.age = 0

    def grow(self):
        self.currEnergy += self.currEnergy * (self.growthRateEnegry / 100)
        self.age += 1

    def survive(self):
        if self.currEnergy < self.minEnergy:
            self.grid.removePlant(self)

    def reproduce(self):
        if self.age % self.reproductionSteps == 0:
            for _ in range(random.randint(1, 5)):       ## Zufall zwischen 1 und 5
                offspringPosition = self.findOffspringPos()
                if offspringPosition:
                    offspring = Plant(species=self.species, 
                                      initEnergy=self.offspringEnergy, 
                                      growthRateEnegry=self.growthRateEnegry, 
                                      minEnegrgy=self.minEnergy, 
                                      reproductionSteps=self.reproductionSteps, 
                                      offspingEnergy=self.offspringEnergy, 
                                      minDist=self.minDist, 
                                      maxDist=self.maxDist, 
                                      position=offspringPosition, 
                                      grid=self.grid
                    )
                    self.grid.addPlant(offspring)
                    self.currEnergy -= 10 # Enegrie aufwenden, um Nachkommen zu produzieren!


    def findOffspringPos(self):
        directions = [(dx, dy) for dx in range(-self.maxDist, self.maxDist+1)
                      for dy in range(-self.maxDist, self.maxDist+1)
                      if self.minDist <= abs(dx) + abs(dy) <= self.maxDist]
        
        random.shuffle(directions)
        for dx, dy in directions:
            newX, newY = self.position[0] + dx, self.position[1] + dy
            if self.grid.isWithinBounds(newX, newY) and not self.grid.isOccupied((newX, newY)):
                return (newX, newY)
        return None   
    
    