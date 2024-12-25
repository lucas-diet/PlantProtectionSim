
import numpy as np
import matplotlib.pyplot as plt

class Diagrams:
    
    def __init__(self, grid):
        self.grid = grid
    
    def plotPlantEnergy(self):
        """_summary_
            Erstellt den Plot für die Pflanzenenergie über die Zeit
        """
        # Erstelle den Plot für Pflanzenenergie
        self.createTimeSeriesPlot(self.grid.energyChanges_plants, 'Plant', 'Energy of Plants Over Time', 'Energy')

    def plotEnemyClusterSize(self):
        """_summary_
            Erstellt den Plot für die Clustergröße der Fressfeinde über die Zeit
        """
        # Erstelle den Plot für Clustergrößen der Fressfeinde
        self.createTimeSeriesPlot(self.grid.sizeChanges_enemies, 'EnemyCluster', 'Size of Enemy-Cluster Over Time', 'Size')

    def createTimeSeriesPlot(self, data_dict, label_type, title, ylabel):
        """_summary_
            Diese Methode gruppiert die Eingabedaten nach Labels (z. B. Pflanzen oder Fressfeinde),
            extrahiert die entsprechenden Werte und erstellt anschließend einen Plot,
            der die Zeitreihe für jedes Label darstellt. Wenn für ein Label keine Werte
            vorhanden sind, wird die Zeitreihe bis zum letzten Zeitpunkt mit Nullen aufgefüllt.
        Args:
            data_dict (dict): Ein Dictionary, das die Daten für die Zeitreihe enthält.
            label_type (str): Ein String, der den Typ des Labels angibt. Kann entweder 'Plant' oder 'EnemyCluster' sein, je nachdem, ob Pflanzen oder Fressfeinde geplottet werden.          
            title (str): Der Titel des Plots, der auf der Grafik angezeigt wird.
            ylabel (str): Der Name der Y-Achse (z.B. 'Energy' oder 'Cluster Size').
    """
        # Schritt 1: Gruppiere die Daten
        grouped_data = self.groupDataByLabel(data_dict)
        
        # Schritt 2: Extrahiere die Werte
        value_arrays = self.extractValues(grouped_data)
        
        # Schritt 3: Erstelle den Plot
        self.plotTimeSeries(value_arrays, grouped_data, label_type, title, ylabel)
    
    def groupDataByLabel(self, data_dict):
        """_summary_
            Gruppiert die Daten nach Label (z.B. Pflanzen oder Fressfeinde).

            Diese Methode erstellt ein Dictionary, das die Daten nach Labels gruppiert,
            wobei jedes Label eine Liste von Zeit-Wert-Paaren enthält.
        Args:
            data_dict (dict): Ein Dictionary mit Schlüsseln als Tupel aus (Label, Zeit) und Werten als den zugehörigen Wert (z.B. Energie oder Clustergröße).
        Returns:
            dict: Ein Dictionary, das Labels als Schlüssel und eine Liste von Zeit-Wert-Paaren als Wert enthält.
        """
        grouped_data = {}
        
        for (label, time), value in data_dict.items():
            if label not in grouped_data:
                grouped_data[label] = []
            grouped_data[label].append((time, value))

        return grouped_data
    
    
    def extractValues(self, grouped_data):
        """_summary_
            Diese Methode erstellt ein Dictionary, das für jedes Label eine Liste der extrahierten Werte 
            (z.B. Energie oder Clustergröße) enthält, die nach Zeitpunkten sortiert sind.
        Args:
            grouped_data (dict): Ein Dictionary, das Labels als Schlüssel und eine Liste von Zeit-Wert-Paaren als Wert enthält.
        Returns:
            dict: Ein Dictionary, das Labels als Schlüssel und eine Liste der extrahierten Werte als Wert enthält.
        """
        value_arrays = {}
        
        for label, changes in grouped_data.items():
            changes.sort(key=lambda x: x[0])  # Sortiere nach Zeitpunkten
            values = [value for time, value in changes]
            value_arrays[label] = values
        
        return value_arrays      
    

    def plotTimeSeries(self, value_arrays, grouped_data, label_type, title, ylabel):
        """_summary_
            Diese Methode erstellt einen Plot für die angegebenen Zeitreihendaten und 
            füllt fehlende Werte mit Nullen auf, sodass die Zeitreihe kontinuierlich bleibt.
        Args:
            value_arrays (dict): Ein Dictionary mit Labels als Schlüssel und Listen von Werten als Werte.
            grouped_data (dict): Ein Dictionary, das Labels als Schlüssel und eine Liste von Zeit-Wert-Paaren als Wert enthält.
            label_type (str): Der Typ des Labels ('Plant' oder 'Enemy').
            title (str): Der Titel des Plots.
            ylabel (str): Die Beschriftung der Y-Achse.
        """
        plt.figure(figsize=(10, 6)) 

        # Bestimme den maximalen Zeitpunkt, um das Ende der Linie mit Null-Werten zu füllen
        all_times = sorted(set(time for times in grouped_data.values() for time, _ in times))

        for label, values in value_arrays.items():
            # Extrahiere die Zeitpunkte für dieses Label
            times = [time for time, value in grouped_data[label]]
            
            # Bestimme den Namen des Labels (Pflanze oder Fressfeind)
            if label_type == 'Plant':
                label_name = label.name
            else:
                label_name = label.enemy.name
            
            # Fülle die Zeitreihe mit Nullen, falls keine Daten vorhanden sind
            filled_values = []
            for t in all_times:
                # Falls für den aktuellen Zeitpunkt ein Wert existiert, füge ihn hinzu, ansonsten 0
                if t in dict(grouped_data[label]):
                    filled_values.append(dict(grouped_data[label])[t])
                else:
                    filled_values.append(0)
            
            # Plot für das Label
            plt.plot(all_times, filled_values, label=f'{label_name}' if label_type == 'Plant' else f'{label_name}')
        
        # Titel und Achsenbeschriftungen
        plt.title(title)
        plt.xlabel('Time')
        plt.xticks(ticks=all_times)
        plt.ylabel(ylabel)
        plt.legend()  # Legende hinzufügen
        plt.grid(True)
        
        plt.show()







        