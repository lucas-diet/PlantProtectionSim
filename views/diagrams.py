
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Setze das Backend für matplot lib, bevor pyplot importiert wird

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk

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


    def fillMissingTimePoints(self, aggregated_data, all_times):
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
        self.fillMissingTimePoints(aggregated_data, all_times)
        self.sortAggregatedData(aggregated_data)
        return aggregated_data


    def dataPlotter(self, data_dict, simLength, measure, title, ylabel=['energy', 'count', 'size', 'count'], root=None):
        """_summary_
            Erstellt einen einzelnen Plot und zeigt ihn entweder in einer GUI oder außerhalb an.
        Args:
            data_dict (dict): Ein Dictionary mit den Daten.
            simLength (int): Die Anzahl der Zeitschritte.
            measure (str): Die zu plottende Messgröße.
            title (str): Titel des Plots.
            ylabel (list, optional): Liste von Beschriftungen der y-Achse.
            root (tk.Widget, optional): Das Tkinter-Widget für die Anzeige in der GUI. Falls None, wird der Plot außerhalb angezeigt.
        """
        aggregated_data = self.aggregateBySpecies(data_dict)
        simArr = list(range(simLength + 1))

        # Matplotlib-Figure erstellen
        fig = Figure(figsize=(11, 5))
        axis = fig.add_subplot(111)

        # Plot erstellen
        total = {}
        for species, measurements in aggregated_data.items():
            if measure in measurements:
                time_series = measurements[measure]
                times, values = zip(*time_series)

                # Fehlende Werte auffüllen
                filled_values = self.fillMissingValues(times, values, simArr)
                axis.plot(simArr, filled_values, label=species)

                # Totale berechnen
                for time, value in time_series:
                    total[time] = total.get(time, 0) + value

        if total:
            total_values = [total.get(time, 0) for time in simArr]
            axis.plot(simArr, total_values, label='Total', linestyle='--', color='black', linewidth=1)

        # Achsen und Titel setzen
        ylabel_text = ylabel.pop(0) if isinstance(ylabel, list) and ylabel else ylabel or 'Value'
        axis.set_title(title)
        axis.set_xlabel('Time')
        axis.set_ylabel(ylabel_text)
        axis.legend(title='Species', loc='center left', bbox_to_anchor=(1.0, 0.5))
        axis.grid(True)

        if root:
            # Plot in das übergebene Widget einfügen
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas.draw()

            # Speicherbutton hinzufügen
            self.save_plot(fig, root)
        else:
            # Plot außerhalb der GUI anzeigen
            plt.figure(figsize=(11, 5))
            for line in axis.lines:
                if line.get_label() == 'Total':
                    # Zeichne den Total-Wert in Schwarz und gestrichelt
                    plt.plot(line.get_xdata(), line.get_ydata(), label=line.get_label(), linestyle='--', color='black', linewidth=1)
                else:
                    plt.plot(line.get_xdata(), line.get_ydata(), label=line.get_label())
            plt.title(title)
            plt.xlabel('Time')
            plt.ylabel(ylabel_text)
            plt.legend(title='Species', loc='center left', bbox_to_anchor=(1.0, 0.5))
            plt.grid(True)
            plt.show()


    def fillMissingValues(self, times, values, simArr):
        """_summary_
            Füllt fehlende Werte in den Daten auf.
        Args:
            times (list): Liste der Zeitpunkte mit Daten.
            values (list): Liste der Messwerte.
            simArr (list): Vollständige Zeitpunkte.
        Returns:
            list: Liste der Messwerte mit aufgefüllten fehlenden Werten.
        """
        return [values[times.index(time)] if time in times else 0 for time in simArr]


    def save_plot(self, fig, root):
        """_summary_
            Fügt eine Schaltfläche zum Speichern des Plots hinzu.
        Args:
            fig (matplotlib.figure.Figure): Die Figur, die gespeichert werden soll.
            root (tk.Tk): Das Tkinter-Hauptfenster.
        """
        def save_action():
            from tkinter.filedialog import asksaveasfilename
            file_path = asksaveasfilename(defaultextension='.png',
                                        filetypes=[('PNG files', '*.png'),
                                                    ('JPEG files', '*.jpg'),
                                                    ('PDF files', '*.pdf'),
                                                    ('All files', '*.*')])
            if file_path:
                fig.savefig(file_path)
                print(f'Plot gespeichert unter: {file_path}')

        save_button = tk.Button(root, text='Save Plot', command=save_action)
        save_button.pack(side=tk.BOTTOM, pady=10)


        