
import matplotlib
matplotlib.use('TkAgg')  # Setze das Backend für matplot lib, bevor pyplot importiert wird
print(matplotlib.get_backend())

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

import matplotlib.pyplot as plt

class Diagrams:
    
    def __init__(self, grid):
        self.grid = grid
    
    
    def collectAllTimes(self, data_dict):
        """_summary_
            Extrahiert alle einzigartigen Zeitpunkte aus den Daten.
        Args:
            data_dict (dict): Ein Dictionary mit Schlüsseln als (Art, Zeit) und Werten.
        Returns:
            set: Eine Menge aller einzigartigen Zeitpunkte.
        """
        return {time for _, time in data_dict.keys()}


    def initializeAggregatedData(self, data_dict):
        """_summary_
            Initialisiert ein Aggregations-Dictionary basierend auf Spezies und Messgrößen.
        Args:
            data_dict (dict): Ein Dictionary mit Schlüsseln (Art, Zeit).
        Returns:
            dict: Ein leeres Aggregations-Dictionary, das nach Spezies und Messgrößen strukturiert ist.
        """
        aggregated_data = {}
        for (species, _), measurements in data_dict.items():
            if species not in aggregated_data:
                aggregated_data[species] = {}
            for measure in measurements.keys():
                if measure not in aggregated_data[species]:
                    aggregated_data[species][measure] = {}
        return aggregated_data


    def populateAggregatedData(self, data_dict, aggregated_data):
        """_summary_
            Füllt das Aggregations-Dictionary mit Werten auf.
        Args:
            data_dict (dict): Ein Dictionary mit Schlüsseln als (Art, Zeit).
            aggregated_data (dict): Ein zuvor initialisiertes Aggregations-Dictionary, das gefüllt werden soll.    
        """
        for (species, time), measurements in data_dict.items():
            for measure, value in measurements.items():
                if time not in aggregated_data[species][measure]:
                    aggregated_data[species][measure][time] = 0
                aggregated_data[species][measure][time] += value


    def fillMissingTimes(self, aggregated_data, all_times):
        """_summary_
            Füllt fehlende Zeitpunkte in den aggregierten Daten mit Null auf.
        Args:
            aggregated_data (dict): Ein Dictionary mit aggregierten Daten, organisiert nach Spezies und Messpunkten.
            all_times (list): Eine sortierte Liste aller Zeitpunkte.
        """
        for species in aggregated_data:
            for measure in aggregated_data[species]:
                for time in all_times:
                    if time not in aggregated_data[species][measure]:
                        aggregated_data[species][measure][time] = 0


    def sortAggregatedData(self, aggregated_data):
        """_summary_
            Sortiert die aggregierten Daten basierend auf den Zeitpunkten.
        Args:
            aggregated_data (dict): Ein Dictionary mit Spezies als Schlüssel und zugehörigen Messwerten nach Zeit.
        """
        for species in aggregated_data:
            for measure in aggregated_data[species]:
                aggregated_data[species][measure] = sorted(aggregated_data[species][measure].items())


    def aggregateBySpecies(self, data_dict):
        """_summary_
            Aggregiert die Werte pro Spezies über die Zeit.
                Schritte:
                1. Alle Zeitpunkte erfassen und sortieren.
                2. Initialisierung der aggregierten Datenstruktur.
                3. Befüllen der aggregierten Datenstruktur mit Werten.
                4. Auffüllen fehlender Zeitpunkte mit Nullwerten.
                5. Sortieren der Daten nach Zeitpunkten.
            Args:
                data_dict (dict): Ein Dictionary mit Schlüsseln als (Spezies, Zeit) und Werten als Dictionary von Messwerten.
            Returns:
                dict: Ein Dictionary mit aggregierten Werten nach Spezies und Zeit. 
        """
        all_times = sorted(self.collectAllTimes(data_dict))
        aggregated_data = self.initializeAggregatedData(data_dict)
        self.populateAggregatedData(data_dict, aggregated_data)
        self.fillMissingTimes(aggregated_data, all_times)
        self.sortAggregatedData(aggregated_data)
        return aggregated_data


    def dataPlotter(self, root, data_dict, simLength, measure1, measure2, title1, title2):
        """
        Plottet zwei verschiedene Messgrößen für mehrere Spezies in separaten Subplots
        in einem Tkinter-Fenster.

        Args:
            root (tk.Tk): Das Tkinter-Hauptfenster oder ein anderes Tkinter-Widget.
            data_dict (dict): Ein Dictionary mit (Spezies, Zeit) als Schlüssel.
            simLength (int): Ist die Anzahl an Zeitschritten, die simuliert werden.
            measure1 (str): Die erste Messgröße ('energy' oder 'size').
            measure2 (str): Die zweite Messgröße ('count').
            title1 (str): Titel des ersten Subplots.
            title2 (str): Titel des zweiten Subplots.
        """
        aggregated_data = self.aggregateBySpecies(data_dict)
        fig = Figure(figsize=(14, 7))
        axes = fig.subplots(2, 1)

        total1 = {}
        total2 = {}

        # Zeitpunkte von 0 bis Ende der Simulation
        simArr = list(range(simLength + 1))

        # Measure1 plotten
        for species, measurements in aggregated_data.items():
            if measure1 in measurements:
                time_series = measurements[measure1]
                times, values = zip(*time_series)

                # Fehlende Werte auffüllen
                filled_values = [values[times.index(time)] if time in times else 0 for time in simArr]
                axes[0].plot(simArr, filled_values, label=species)
                for time, value in time_series:
                    total1[time] = total1.get(time, 0) + value

        if total1:
            total_values = [total1.get(time, 0) for time in simArr]
            axes[0].plot(simArr, total_values, label='Total', linestyle='--', color='black', linewidth=1)

        axes[0].set_title(title1)
        axes[0].set_xlabel('Time')
        axes[0].set_xticks(simArr)
        axes[0].set_ylabel(measure1.capitalize())
        axes[0].legend(title='Species', loc='center left', bbox_to_anchor=(1.0, 0.5))
        axes[0].grid(True)

        # Measure2 plotten
        for species, measurements in aggregated_data.items():
            if measure2 in measurements:
                time_series = measurements[measure2]
                times, values = zip(*time_series)

                # Fehlende Werte auffüllen
                filled_values = [values[times.index(time)] if time in times else 0 for time in simArr]
                axes[1].plot(simArr, filled_values, label=species)
                for time, value in time_series:
                    total2[time] = total2.get(time, 0) + value

        if total2:
            total_values = [total2.get(time, 0) for time in simArr]
            axes[1].plot(simArr, total_values, label='Total', linestyle='--', color='black', linewidth=1)

        axes[1].set_title(title2)
        axes[1].set_xlabel('Time')
        axes[1].set_xticks(simArr)
        axes[1].set_ylabel(measure2.capitalize())
        axes[1].legend(title='Species', loc='center left', bbox_to_anchor=(1.0, 0.5))
        axes[1].grid(True)

        # Abstand zwischen den Subplots erhöhen
        fig.subplots_adjust(hspace=0.5)

        # Speichern-Funktion
        def save_plot():
            from tkinter.filedialog import asksaveasfilename
            file_path = asksaveasfilename(defaultextension='.png', 
                                            filetypes=[('PNG files', '*.png'),
                                                    ('JPEG files', '*.jpg'),
                                                    ('PDF files', '*.pdf'),
                                                    ('All files', '*.*')])
            if file_path:
                fig.savefig(file_path)
                print(f'Plot gespeichert unter: {file_path}')

        # Speichern-Schaltfläche hinzufügen
        save_button = tk.Button(root, text='Save Plot', command=save_plot)
        save_button.pack(side=tk.BOTTOM, pady=10)


        # Matplotlib-Canvas in Tkinter-Fenster einbinden
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Canvas zeichnen
        canvas.draw()

    