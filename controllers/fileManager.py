

import pickle as pkl


class Exporter():

    def __init__(self, path, grid):
        self.path =  path
        self.grid = grid

    
    def getDate(self):
        grid = self.grid
        plants = self.grid.plants
        cluster = self.grid.enemies
        signals = self.grid.signals
        toxins = self.grid.toxins

        # Verbindungen aus Pflanzen extrahieren
        plant_connections = {plant.name: plant.gridConnections for plant in plants}

        return {'grid': grid, 'plants': plants, 'cluster': cluster, 'signals': signals, 'toxins': toxins, 'connections': plant_connections}
    

    def save(self):
        data = self.getDate()
        try:
            with open(self.path, 'wb') as file:
                pkl.dump(data, file)
        except Exception as e:
            print(f'Fehler beim Speichern der Daten {e}')



class Importer():

    def __init__(self, path):
        self.path = path

    
    def load(self):
        with open(self.path, 'rb') as file:
            data = pkl.load(file)
        
        grid = self.reconstructData(data)
        return grid

    
    def reconstructData(self, data):
        grid = data['grid']
        
        # Pflanzen hinzufügen
        for plant in data['plants']:
            if plant not in grid.plants:
                grid.addPlant(plant)

        # Feinde hinzufügen
        for ec in data['cluster']:
            if ec not in grid.enemies:
                grid.addEnemies(ec)

        # Signale hinzufügen
        for signal in data['signals']:
            if signal not in grid.signals:
                grid.addSubstance(signal)

        # Toxine hinzufügen
        for toxin in data['toxins']:
            if toxin not in grid.toxins:
                grid.addSubstance(toxin)

        # Symbiotische Verbindungen herstellen
        for pName, connection in data['connections'].items():
            plant = self.getPlantByName(pName, grid)
            if plant:
                plant.gridConnections = connection

        return grid


    def getPlantByName(self, name, grid):
        for plant in grid.plants:
            if plant.name == name:
                return plant
        return None
        

