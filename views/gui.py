
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import threading
from concurrent.futures import ThreadPoolExecutor
import random

from models.grid import Grid
from models.plant import Plant
from models.enemyCluster import Enemy, EnemyCluster
from controllers.simulation import Simulation
from views.diagrams import Diagrams
from models.connection import SymbioticConnection
from models.substance import Substance
from models.signal import Signal
from models.toxin import Toxin


class Gui():

	def __init__(self):
		self.initSimulationWindow()
		self.set_breakupsAuto()

		self.PLANT_COLORS = ['#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']
		self.selectedItem = tk.IntVar(value=-1)
		
		self.players = []
		self.enemies_at_positions = {}
		self.plant_at_position = {}
		self.lock = threading.Lock()
		self.plant_connections = {}
		self.grid_lines = {}
		self.valid_substances_set = set()
		self.last_plant_colors = {}


	def initSimulationWindow(self):
		self.root = tk.Tk()
		self.root.title('Simulator')
		# Berechnen der Fenstergröße
		window_width = self.root.winfo_screenwidth() - 200
		window_height = self.root.winfo_screenheight() - 200
		
		# Berechnung der Position, um das Fenster zu zentrieren
		center_x = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
		center_y = int(self.root.winfo_screenheight() / 2 - window_height / 2)
		
		# Setzen der Fenstergröße und Position
		self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

		self.createWindowAreas()


	def mainloop(self):
		self.root.mainloop()


	def createWindowAreas(self):
		# Bereich oben
		self.top_frame = tk.Frame(self.root)
		self.top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
		self.topAreaWidgets()
		
		# Bereich links (Sidebar)
		self.left_frame = tk.Frame(self.root, bg='lightgreen')
		self.left_frame.grid(row=1, column=0, sticky='nsew')
		
		# Tabs in der Sidebar
		self.sidebarTabs()
		
		# Bereich rechts
		self.right_frame = tk.Frame(self.root, padx=5, pady=5)
		self.right_frame.grid(row=1, column=1, sticky='nsew')
		
		
		# Spalten und Zeilen skalierbar machen
		self.root.grid_rowconfigure(0, weight=0)  # Oben
		self.root.grid_rowconfigure(1, weight=6)  # Mitte
		self.root.grid_columnconfigure(0, weight=2)  # Links
		self.root.grid_columnconfigure(1, weight=9, uniform='equal')  # Rechts
	
	
	def topAreaWidgets(self):
		"""Erstellt die Widgets im oberen Bereich."""
		# Gridgröße
		tk.Label(self.top_frame, text='Grid-Size:').grid(row=0, column=0, padx=1, pady=1, sticky='w')
		self.grid_size_entry = tk.Entry(self.top_frame, width=10)
		self.grid_size_entry.grid(row=0, column=1, padx=1, pady=1, sticky='ew')
		
		# Pflanzen
		tk.Label(self.top_frame, text='#Plants:').grid(row=0, column=2, padx=1, pady=1, sticky='w')
		self.plants_entry = tk.Entry(self.top_frame, width=10)
		self.plants_entry.grid(row=0, column=3, padx=1, pady=1, sticky='ew')
		
		# Fressfeinde
		tk.Label(self.top_frame, text='#Enemies:').grid(row=0, column=4, padx=1, pady=1, sticky='w')
		self.enemies_entry = tk.Entry(self.top_frame, width=10)
		self.enemies_entry.grid(row=0, column=5, padx=1, pady=1, sticky='ew')
		
		# Substanzen
		tk.Label(self.top_frame, text='#Substances:').grid(row=0, column=6, padx=1, pady=1, sticky='w')
		self.substances_entry = tk.Entry(self.top_frame, width=10)
		self.substances_entry.grid(row=0, column=7, padx=1, pady=1, sticky='ew')
		
		# Buttons
		tk.Button(self.top_frame, text='Apply', command=self.createSituation).grid(row=0, column=8, columnspan=1, pady=1)
		
		tk.Label(self.top_frame, text=' ', width=4).grid(row=0, column=9, padx=1, pady=1, sticky='ew')
		
		tk.Button(self.top_frame, text='Breakups', command=self.open_breakupWindow).grid(row=0, column=10, columnspan=1, pady=1, sticky='ew')
		tk.Button(self.top_frame, text='Play', command=self.start_simulation).grid(row=0, column=11, columnspan=1, pady=1, sticky='ew') ######################################

		self.roundCount = tk.Label(self.top_frame, text='0', width=4, bg='red')
		self.roundCount.grid(row=0, column=12, padx=1, pady=1, sticky='ew')

		tk.Button(self.top_frame, text='Plot', command=self.open_plotWindow).grid(row=0, column=13, columnspan=1, pady=1, sticky='ew')

		tk.Button(self.top_frame, text='Import').grid(row=0, column=14, columnspan=1, pady=1, sticky='ew')
		tk.Button(self.top_frame, text='Export').grid(row=0, column=15, columnspan=1, pady=1, sticky='ew')


	def createSituation(self):
		self.input_plantsTab()
		self.input_enemiesTab()
		self.input_substancesTab()
		self.input_gridSize()

		self.roundCount.config(text='0', bg='red')
	

	def sidebarTabs(self):
		"""Erstellt Tabs für die Sidebar."""
		# Notebook für Tabs
		self.sidebar_tabs = ttk.Notebook(self.left_frame)
		
		# Tab 1: Pflanzen
		self.plants_tab = tk.Frame(self.sidebar_tabs)
		self.plants_tab.pack(fill='both', expand=True)
		self.sidebar_tabs.add(self.plants_tab, text='Plants')
		
		# Tab 2: Feinde
		self.enemies_tab = tk.Frame(self.sidebar_tabs)
		self.sidebar_tabs.add(self.enemies_tab, text='Enemies')
		
		# Tab 3: Substanzen
		self.substances_tab = tk.Frame(self.sidebar_tabs)
		self.sidebar_tabs.add(self.substances_tab, text='Substances')
		
		# Packe das Notebook in die Sidebar
		self.sidebar_tabs.pack(fill='both', expand=True)

	
	def input_plantsTab(self):
		try:
			# Eingabe in eine Zahl umwandeln
			number_of_plants = int(self.plants_entry.get())
		except ValueError:
			messagebox.showerror('Invalid input', 'Please enter a valid number')
			# Fehlerbehandlung, falls die Eingabe keine gültige Zahl ist
			return
		
		# Überprüfen, ob die Zahl zwischen 0 und 16 liegt
		if number_of_plants < 1 or number_of_plants > 16:
			self.clear_plantsFrame()  # Lösche bestehende Elemente
			messagebox.showwarning('Invalid number', 'The number of plants must be between 1 and 16!')
			return
		
		# Bereinigen bestehender Widgets, falls die Frame bereits existiert
		if hasattr(self, 'plants_setting_frame'):
			self.clear_plantsFrame()
		else:
			# Erstellen von Canvas, Frame und Scrollbar
			self.plantsCanvasFrame()
		# Substanzen-Einstellungen erstellen
		self.create_plantsSettings(number_of_plants)
	

	def input_enemiesTab(self):
		try:
			# Eingabe in eine Zahl umwandeln
			number_of_enemies = int(self.enemies_entry.get())
		except ValueError:
			# Fehlerbehandlung, falls die Eingabe keine gültige Zahl ist
			messagebox.showerror('Invalid input', 'Please enter a valid number')
			return
		
		# Überprüfen, ob die Zahl zwischen 0 und 15 liegt
		if number_of_enemies < 0 or number_of_enemies > 15:
			self.clear_enemiesFrame()  # Lösche bestehende Elemente
			messagebox.showwarning('Invalid number', 'The number of enemies must be between 0 and 15!')
			return
		
		# Bereinigen bestehender Widgets, falls die Frame bereits existiert
		if hasattr(self, 'enemies_setting_frame'):
			self.clear_enemiesFrame()
		else:
			# Erstellen von Canvas, Frame und Scrollbar
			self.enemiesCanvasFrame()
		# Substanzen-Einstellungen erstellen
		self.create_enemiesSettings(number_of_enemies)

	
	def input_substancesTab(self):
		try:
			# Eingabe in eine Zahl umwandeln
			number_of_substances = int(self.substances_entry.get())
		except ValueError:
			# Fehlerbehandlung, falls die Eingabe keine gültige Zahl ist
			messagebox.showerror('Invalid input', 'Please enter a valid number')
			return
		
		# Überprüfen, ob die Zahl zwischen 0 und 15 liegt
		if number_of_substances < 0 or number_of_substances > 15:
			self.clear_substancesFrame()  # Lösche bestehende Elemente
			messagebox.showwarning('Invalid number', 'The number of substances must be between 0 and 15!')
			return
		
		# Bereinigen bestehender Widgets, falls die Frame bereits existiert
		if hasattr(self, 'substances_setting_frame'):
			self.clear_substancesFrame()
		else:
			# Erstellen von Canvas, Frame und Scrollbar
			self.substancesCanvasFrame()
			
		# Substanzen-Einstellungen erstellen
		self.create_substancesSettings(number_of_substances)


	def input_gridSize(self):
		try:
			gridSize = int(self.grid_size_entry.get())
		except ValueError:
			messagebox.showerror('Invalid input', 'Please enter a valid number')
			return

		if gridSize < 1 or gridSize > 80:
			messagebox.showwarning('Invalid number', 'The number of gridsize must be between 1 and 80!')
			return
		else:
			self.grid = Grid(gridSize, gridSize)
		
		self.clear_gridFrame()
		self.create_gridFrame(gridSize, gridSize)

	
	def clear_plantsFrame(self):
		"""Bereinigt alle Widgets im Frame der Substanzen"""
		if hasattr(self, 'plants_setting_frame'):
			for widget in self.plants_setting_frame.winfo_children():
				widget.destroy()
	

	def clear_enemiesFrame(self):
		"""Bereinigt alle Widgets im Frame der Substanzen"""
		if hasattr(self, 'enemies_setting_frame'):
			for widget in self.enemies_setting_frame.winfo_children():
				widget.destroy()


	def clear_substancesFrame(self):
		"""Bereinigt alle Widgets im Frame der Substanzen"""
		if hasattr(self, 'substances_setting_frame'):
			for widget in self.substances_setting_frame.winfo_children():
				widget.destroy()


	def clear_gridFrame(self):
		if hasattr(self, 'grid_frame'):
			# Zerstöre alle Kinder-Widgets im Frame
			for widget in self.grid_frame.winfo_children():
				widget.destroy()
			# Lösche den Frame selbst
			self.grid_frame.destroy()
			del self.grid_frame  # Entferne die Referenz auf das Attribut


	def plantsCanvasFrame(self):
		# Canvas erstellen und konfigurieren
		self.plants_setting_canvas = tk.Canvas(self.plants_tab, width=0)
		self.plants_setting_canvas.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
		
		# Frame erstellen und im Canvas einfügen
		self.plants_setting_frame = tk.Frame(self.plants_setting_canvas)
		self.plants_setting_canvas.create_window((0, 0), window=self.plants_setting_frame, anchor='nw')
		
		# Scrollbar erstellen und mit dem Canvas verbinden
		self.plants_scrollbar = tk.Scrollbar(self.plants_tab, orient='vertical', command=self.plants_setting_canvas.yview)
		self.plants_scrollbar.grid(row=0, column=1, sticky='ns', pady=0)
		
		# Scrollbar an Canvas binden (nicht an Frame)
		self.plants_setting_canvas.config(yscrollcommand=self.plants_scrollbar.set, highlightthickness=0)
		
		# Layout-Anpassung für den Canvas und Scrollbar
		self.plants_tab.grid_rowconfigure(0, weight=1)
		self.plants_tab.grid_columnconfigure(0, weight=1)

	
	def enemiesCanvasFrame(self):
		# Canvas erstellen und konfigurieren
		self.enemies_setting_canvas = tk.Canvas(self.enemies_tab, width=0)
		self.enemies_setting_canvas.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
		
		# Frame erstellen und im Canvas einfügen
		self.enemies_setting_frame = tk.Frame(self.enemies_setting_canvas)
		self.enemies_setting_canvas.create_window((0, 0), window=self.enemies_setting_frame, anchor='nw')
		
		# Scrollbar erstellen und mit dem Canvas verbinden
		self.enemies_scrollbar = tk.Scrollbar(self.enemies_tab, orient='vertical', command=self.enemies_setting_canvas.yview)
		self.enemies_scrollbar.grid(row=0, column=1, sticky='ns', pady=0)
		
		# Scrollbar an Canvas binden (nicht an Frame)
		self.enemies_setting_canvas.config(yscrollcommand=self.enemies_scrollbar.set, highlightthickness=0)
		
		# Layout-Anpassung für den Canvas und Scrollbar
		self.enemies_tab.grid_rowconfigure(0, weight=1)
		self.enemies_tab.grid_columnconfigure(0, weight=1)


	def substancesCanvasFrame(self):
		# Canvas erstellen und konfigurieren
		self.substances_setting_canvas = tk.Canvas(self.substances_tab, width=0)
		self.substances_setting_canvas.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)
		
		# Frame erstellen und im Canvas einfügen
		self.substances_setting_frame = tk.Frame(self.substances_setting_canvas)
		self.substances_setting_canvas.create_window((0, 0), window=self.substances_setting_frame, anchor='nw')
		
		# Scrollbar erstellen und mit dem Canvas verbinden
		self.substances_scrollbar = tk.Scrollbar(self.substances_tab, orient='vertical', command=self.substances_setting_canvas.yview)
		self.substances_scrollbar.grid(row=0, column=1, sticky='ns', pady=0)
		
		# Scrollbar an Canvas binden (nicht an Frame)
		self.substances_setting_canvas.config(yscrollcommand=self.substances_scrollbar.set, highlightthickness=0)
		
		# Layout-Anpassung für den Canvas und Scrollbar
		self.substances_tab.grid_rowconfigure(0, weight=1)
		self.substances_tab.grid_columnconfigure(0, weight=1)
	

	def create_plantsSettings(self, number_of_plants):
		"""Erstellt die Einstellungen für Pflanzen."""
		
		# Label für Abstand
		tk.Label(self.plants_setting_frame, text='', width=25).grid(row=0, column=4, padx=1, pady=1, sticky='w')
		
		# Gemeinsame Variable für alle Checkbuttons
		if not hasattr(self, 'selectedPlayer'):
			self.selectedPlayer = tk.IntVar(value=-1)  # -1 bedeutet: Kein Button ausgewählt
		
		# Dictionaries für Eingabefelder für jede Pflanze
		self.plant_entries = {}  # Hier speichern wir die Eingabefelder für jede Pflanze
		#Fehlermeldung wenn Eingabe nicht korrekt ist
		self.error_plants = tk.Label(self.plants_setting_frame, text='')
		self.error_plants.grid(row=0, column=0, columnspan=5, sticky='w', padx=2, pady=2)
				
		for i in range(number_of_plants):
			row = i * 7
		
			# Checkbutton für Pflanze
			plant_checkbox = tk.Checkbutton(
				self.plants_setting_frame,
				variable=self.selectedItem,  # Gemeinsame Variable
				onvalue=i,  # Wert, wenn dieser Checkbutton ausgewählt wird
				offvalue=-1,  # Wert, wenn kein Checkbutton ausgewählt ist
				text=f'Plant {i+1}:'
			)
			plant_checkbox.grid(row=row+1, column=0, sticky='w', padx=2, pady=2)
			
			# Farbe der Pflanze
			plant_color_label = tk.Label(self.plants_setting_frame, width=2, bg=self.PLANT_COLORS[i])
			plant_color_label.grid(row=row+1, column=1, sticky='ew', padx=2, pady=2)
			
			# Energie-Label und Eingabefelder
			initEnergy_label = tk.Label(self.plants_setting_frame, text='Init-Energy:')
			initEnergy_label.grid(row=row+2, column=0, sticky='w', padx=2, pady=2)
			self.plant_entries[i] = {}  # Erstelle einen Dictionary für die Eingabewerte dieser Pflanze
			self.plant_entries[i]['initEnergy'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['initEnergy'].grid(row=row+2, column=1, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.plant_entries[i]['initEnergy'], 'Initial energy level of the plant e.g. 100.')

			growEnergy_label = tk.Label(self.plants_setting_frame, text='Growth-Rate:')
			growEnergy_label.grid(row=row+2, column=2, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['growthRate'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['growthRate'].grid(row=row+2, column=3, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.plant_entries[i]['growthRate'], 'Growth rate of energy e.g. 1')
			
			minEnergy_label = tk.Label(self.plants_setting_frame, text='Min-Energy:')
			minEnergy_label.grid(row=row+3, column=0, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['minEnergy'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['minEnergy'].grid(row=row+3, column=1, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.plant_entries[i]['minEnergy'], 'Minimum energy for survival e.g. 50')
			
			repInter_label = tk.Label(self.plants_setting_frame, text='Repro-Interval:')
			repInter_label.grid(row=row+4, column=0, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['reproInterval'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['reproInterval'].grid(row=row+4, column=1, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.plant_entries[i]['reproInterval'], 'Number of steps until plant reproduces e.g. 10')

			offspringEnergy_label = tk.Label(self.plants_setting_frame, text='Offspring-Energy:')
			offspringEnergy_label.grid(row=row+4, column=2, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['offspring'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['offspring'].grid(row=row+4, column=3, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.plant_entries[i]['offspring'], 'Initial energy level of offspring e.g. 90')
			
			minDist_label = tk.Label(self.plants_setting_frame, text='Min-Distance:')
			minDist_label.grid(row=row+5, column=0, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['minDist'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['minDist'].grid(row=row+5, column=1, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.plant_entries[i]['minDist'], 'Minimum range for offspring e.g. 2')
			
			maxDist_label = tk.Label(self.plants_setting_frame, text='Max-Distance:')
			maxDist_label.grid(row=row+5, column=2, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['maxDist'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['maxDist'].grid(row=row+5, column=3, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.plant_entries[i]['maxDist'], 'Maximum range for offspring e.g. 5')
			
			# Platzhalter für Abstand
			space_label = tk.Label(self.plants_setting_frame, width=4)
			space_label.grid(row=row+6, column=0, padx=2, pady=2, sticky='w')
		
		# Scrollregion aktualisieren
		self.plants_setting_frame.update_idletasks()
		self.plants_setting_frame.bind('<Configure>', lambda e: self.update_scrollregion(self.plants_setting_canvas))
				
	
	def create_enemiesSettings(self, number_of_enemies):
		tk.Label(self.enemies_setting_frame, text='', width=25).grid(row=0, column=4, padx=1, pady=1, sticky='w')
		offset = 16  # Offset, um die Feinde von den Pflanzen in der Variablen zu unterscheiden
		
		self.enemy_entries = {}
		self.error_enemies = tk.Label(self.enemies_setting_frame, text='')
		self.error_enemies.grid(row=0, column=0, columnspan=5, sticky='w', padx=2, pady=2)

		# Mapping für die Indizes erstellen
		self.enemy_index_mapping = {}

		for i in range(number_of_enemies):
			row = i * 10
			
			# Mapping hinzufügen
			self.enemy_index_mapping[offset + i] = i
			
			# Checkbutton für Feind
			enemy_checkbox = tk.Checkbutton(
				self.enemies_setting_frame,
				variable=self.selectedItem,  # Gemeinsame Variable
				onvalue=offset + i,  # Ein eindeutiger Wert für Feinde
				offvalue=-1,  # Wert, wenn kein Checkbutton ausgewählt ist
				text=f'Enemy {i+1}:'
			)
			enemy_checkbox.grid(row=row+1, column=0, sticky='w', padx=2, pady=2)
			self.enemy_entries[i] = {}

			clusterNum_label = tk.Label(self.enemies_setting_frame, text='Cluster-Size:')
			clusterNum_label.grid(row=row+2, column=0, sticky='w', padx=2, pady=2)
			self.enemy_entries[i]['clusterSize'] = tk.Entry(self.enemies_setting_frame, width=4)
			self.enemy_entries[i]['clusterSize'].grid(row=row+2, column=1, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.enemy_entries[i]['clusterSize'], 'Number of individuals in a cluster e.g. 10')
			
			speed_label = tk.Label(self.enemies_setting_frame, text='Speed:')
			speed_label.grid(row=row+2, column=2, sticky='w', padx=2, pady=2)
			self.enemy_entries[i]['speed'] = tk.Entry(self.enemies_setting_frame, width=4)
			self.enemy_entries[i]['speed'].grid(row=row+2, column=3, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.enemy_entries[i]['speed'], 'Running speed how many time steps are needed for one step e.g 2')
			
			eatingSpeed_label = tk.Label(self.enemies_setting_frame, text='Eat-Speed:')
			eatingSpeed_label.grid(row=row+3, column=0, sticky='w', padx=2, pady=2)
			self.enemy_entries[i]['eatSpeed'] = tk.Entry(self.enemies_setting_frame, width=4)
			self.enemy_entries[i]['eatSpeed'].grid(row=row+3, column=1, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.enemy_entries[i]['eatSpeed'], 'number of energy units eaten per time step e.g. 2')
			
			eatingVic_label = tk.Label(self.enemies_setting_frame, text='Eat-Victory:')
			eatingVic_label.grid(row=row+3, column=2, sticky='w', padx=2, pady=2)
			self.enemy_entries[i]['eatVictory'] = tk.Entry(self.enemies_setting_frame, width=4)
			self.enemy_entries[i]['eatVictory'].grid(row=row+3, column=3, sticky='ew', padx=2, pady=2)

			self.create_tooltip_inputs(self.enemy_entries[i]['eatVictory'], 'Energy units required to produce an offspring, e.g. 2')
			
			space_label = tk.Label(self.enemies_setting_frame, width=4)
			space_label.grid(row=row+4, column=0, padx=2, pady=2, sticky='w')
			
		self.enemies_setting_frame.update_idletasks()
		self.enemies_setting_frame.bind('<Configure>', lambda e: self.update_scrollregion(self.enemies_setting_canvas))


	def create_substancesSettings(self, number_of_substances):
		tk.Label(self.substances_setting_frame, text='', width=15).grid(row=0, column=5, padx=1, pady=1, sticky='w')

		self.substance_entries = {}

		self.error_substances = tk.Label(self.substances_setting_frame, text='')
		self.error_substances.grid(row=0, column=0, columnspan=5, sticky='w', padx=2, pady=2)
		
		for i in range(number_of_substances):
			row = i * 12
			
			# Flachere Struktur: Direkt die Widgets in `self.substance_entries[i]` speichern
			self.substance_entries[i] = {}

			# Checkbox und Dropdown für Substanztyp
			self.substance_entries[i]['checkbox_var'] = tk.IntVar()  # Variable für Checkbox
			substance_beckbox = tk.Checkbutton(
				self.substances_setting_frame,
				text=f'Substance {i+1}:',
				variable=self.substance_entries[i]['checkbox_var']
			)
			substance_beckbox.grid(row=row+1, column=0, sticky='w', padx=2, pady=2)

			substance_options = ['Signal', 'Toxin']
			self.substance_entries[i]['type_var'] = tk.StringVar()
			self.substance_entries[i]['type_var'].set(substance_options[0])

			substanceType_om = tk.OptionMenu(
				self.substances_setting_frame, 
				self.substance_entries[i]['type_var'], 
				*substance_options
			)
			substanceType_om.grid(row=row+1, column=1, padx=2, pady=2, sticky='w')
			substanceType_om.config(fg='black', width=5)
			
			self.substance_entries[i]['toxinEffect_var'] = tk.IntVar()
			self.substance_entries[i]['toxinEffect'] = tk.Checkbutton(
				self.substances_setting_frame, 
				text='Deadly Toxin',
				variable=self.substance_entries[i]['toxinEffect_var'])
			
			self.substance_entries[i]['toxinEffect'].grid(row=row+1, column=2, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['toxinEffect'].config(state='disable')
			
			# Spread-Type Dropdown
			spreadType_label = tk.Label(self.substances_setting_frame, text='Spread:')
			spreadType_label.grid(row=row+2, column=0, padx=2, pady=2, sticky='w')

			substance_spreadtype_options = ['Symbiotic', 'Air']
			self.substance_entries[i]['spreadType_var'] = tk.StringVar()
			self.substance_entries[i]['spreadType_var'].set(substance_spreadtype_options[0])

			substance_spredType_om = tk.OptionMenu(
				self.substances_setting_frame, 
				self.substance_entries[i]['spreadType_var'], 
				*substance_spreadtype_options)
			
			substance_spredType_om.grid(row=row+2, column=1, padx=2, pady=2, sticky='w')
			substance_spredType_om.config(fg='black', width=5)

		
			# Name Eingabefeld
			name_label = tk.Label(self.substances_setting_frame, text='Name:')
			name_label.grid(row=row+3, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['subName'] = tk.Entry(self.substances_setting_frame)
			self.substance_entries[i]['subName'].grid(row=row+3, column=1, columnspan=4, padx=2, pady=2, sticky='ew')

			self.create_tooltip_inputs(self.substance_entries[i]['subName'], 'Name of the substance e.g. methyl jasmonate')

			# Producer Eingabefeld
			emit_label = tk.Label(self.substances_setting_frame, text='Producer:')
			emit_label.grid(row=row+4, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['producer'] = tk.Entry(self.substances_setting_frame)
			self.substance_entries[i]['producer'].grid(row=row+4, column=1, columnspan=4, padx=2, pady=2, sticky='ew')

			self.create_tooltip_inputs(self.substance_entries[i]['producer'], 'Plants that can produce the substances e.g. p1, p2, p5')

			# Receiver Eingabefeld
			receive_label = tk.Label(self.substances_setting_frame, text='Receiver:')
			receive_label.grid(row=row+5, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['receiver'] = tk.Entry(self.substances_setting_frame)
			self.substance_entries[i]['receiver'].grid(row=row+5, column=1, columnspan=4, padx=2, pady=2, sticky='ew')

			self.create_tooltip_inputs(self.substance_entries[i]['receiver'], 'Plants that can receive the substances e.g. p3, p6')

			# Trigger Eingabefeld
			trigger_label = tk.Label(self.substances_setting_frame, text='Trigger:')
			trigger_label.grid(row=row+6, column=0, columnspan=1, padx=2, pady=1, sticky='w')
			self.substance_entries[i]['trigger'] = tk.Entry(self.substances_setting_frame)
			self.substance_entries[i]['trigger'].grid(row=row+6, column=1, columnspan=4, padx=2, pady=2, sticky='ew')

			self.create_tooltip_inputs(self.substance_entries[i]['trigger'], 'Combination that triggers a signaling substance or a toxic substance:\n - Signaling substance: e1,2; e3,5\n - Toxic substance: -signal-name1-,e1,2; -signal-name2-,e3,5')

			# Prod-Time Eingabefeld
			prodTime_label = tk.Label(self.substances_setting_frame, text='Prod-Time:')
			prodTime_label.grid(row=row+7, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['prodTime'] = tk.Entry(self.substances_setting_frame, width=4)
			self.substance_entries[i]['prodTime'].grid(row=row+7, column=1, columnspan=1, padx=2, pady=2, sticky='w')

			self.create_tooltip_inputs(self.substance_entries[i]['prodTime'], 'required time steps to produce the substance e.g. 5.')

			# Send-Speed Eingabefeld
			sendSpeed_label = tk.Label(self.substances_setting_frame, text='Send-Speed:')
			sendSpeed_label.grid(row=row+7, column=2, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['sendSpeed'] = tk.Entry(self.substances_setting_frame, width=4)
			self.substance_entries[i]['sendSpeed'].grid(row=row+7, column=3, columnspan=1, padx=2, pady=2, sticky='w')

			self.create_tooltip_inputs(self.substance_entries[i]['sendSpeed'], 'Time steps required to send the signal substance e.g. 4\n\nA poison is only local to the plant and is not sent - Entry is blocked')

			# Energy-Costs Eingabefeld
			eCosts_label = tk.Label(self.substances_setting_frame, text='Energy-Costs:')
			eCosts_label.grid(row=row+8, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['energyCosts'] = tk.Entry(self.substances_setting_frame, width=4)
			self.substance_entries[i]['energyCosts'].grid(row=row+8, column=1, columnspan=1, padx=2, pady=2, sticky='w')

			self.create_tooltip_inputs(self.substance_entries[i]['energyCosts'], 'Required energy costs that are deducted per time step e.g. 5')

			# AftereffectTime Eingabefeld
			aft_label = tk.Label(self.substances_setting_frame, text='AfterEffectTime:')
			aft_label.grid(row=row+8, column=2, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['aft'] = tk.Entry(self.substances_setting_frame, width=4)
			self.substance_entries[i]['aft'].grid(row=row+8, column=3, columnspan=1, padx=2, pady=2, sticky='w')

			self.create_tooltip_inputs(self.substance_entries[i]['aft'], 'Number of time steps for how long a signaling substance has an aftereffect after its production has ended, e.g. 5\n\nA poisonous substance has no aftereffect time - Entry is blocked')

			eliStrength_label = tk.Label(self.substances_setting_frame, text='Eli-Strength:')
			eliStrength_label.grid(row=row+9, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['eliStrength'] = tk.Entry(self.substances_setting_frame, width=4)
			self.substance_entries[i]['eliStrength'].grid(row=row+9, column=1, columnspan=1, padx=2, pady=2, sticky='w')
			self.substance_entries[i]['eliStrength'].config(state='disable')

			self.create_tooltip_inputs(self.substance_entries[i]['eliStrength'], 'Number of individuals that die per time step if the poison is lethal e.g. 3')

			space_label = tk.Label(self.substances_setting_frame, width=4)
			space_label.grid(row=row+10, column=0, padx=2, pady=2, sticky='w')

			# Instanzvariablen für die Felder speichern
			setattr(self, f'substance_var_{i}', self.substance_entries[i]['type_var'])
			setattr(self, f'substance_menu_{i}', substanceType_om)
			setattr(self, f'toxin_effect_checkbox_{i}', self.substance_entries[i]['toxinEffect'])
			setattr(self, f'substance_spreadtype_menu_{i}', substance_spredType_om)
			setattr(self, f'receive_entry_{i}', self.substance_entries[i]['receiver'])
			setattr(self, f'sendSpeed_entry_{i}', self.substance_entries[i]['sendSpeed'])
			setattr(self, f'aft_entry_{i}', self.substance_entries[i]['aft'])
			setattr(self, f'eli_entry_{i}', self.substance_entries[i]['eliStrength'])

			# Ereignis an Substanzmenü binden
			self.substance_entries[i]['type_var'].trace_add('write', lambda *args, i=i: self.change_SubstanceType(i))
			
		self.substances_setting_frame.update_idletasks()
		# Scrollregion aktualisieren
		self.substances_setting_frame.bind('<Configure>', lambda e: self.update_scrollregion(self.substances_setting_canvas))


	def change_SubstanceType(self, index):
		# Zugriff auf Instanzvariablen basierend auf dem Index
		substance_var = getattr(self, f'substance_var_{index}')
		substance_spreadtype_menu = getattr(self, f'substance_spreadtype_menu_{index}')
		toxin_effect_checkbox = getattr(self, f'toxin_effect_checkbox_{index}')
		receive_entry = getattr(self, f'receive_entry_{index}')
		sendSpeed_entry = getattr(self, f'sendSpeed_entry_{index}')
		aft_entry = getattr(self, f'aft_entry_{index}')
		eli_stren_entry = getattr(self, f'eli_entry_{index}')

		# Disable or enable fields based on the substance type
		if substance_var.get() == 'Toxin':
			substance_spreadtype_menu.config(state='disabled')
			sendSpeed_entry.delete(0, tk.END)
			sendSpeed_entry.config(state='disabled')
			toxin_effect_checkbox.config(state='normal')
			receive_entry.delete(0, tk.END)
			receive_entry.config(state='disable')
			aft_entry.delete(0, tk.END)
			aft_entry.config(state='disabled')
			eli_stren_entry.config(state='normal')
			
		else:
			substance_spreadtype_menu.config(state='normal')
			sendSpeed_entry.config(state='normal')
			toxin_effect_checkbox.config(state='disable')
			receive_entry.config(state='normal')
			aft_entry.config(state='normal')
			eli_stren_entry.delete(0, tk.END)
			eli_stren_entry.config(state='disable')

	
	def create_tooltip_inputs(self, widget, text):
		"""
		Zeigt den Tooltip über einem Eingabefeld an, wenn die Maus darüber fährt.
		"""
		tooltip_window = None  # Variable für das Tooltip-Fenster

		# Funktion zum Anzeigen des Tooltips
		def show_tooltip(event):
			nonlocal tooltip_window

			if tooltip_window is not None:
				return  # Verhindert mehrfaches Erstellen von Tooltips

			# Erstelle ein neues Fenster für den Tooltip
			tooltip_window = tk.Toplevel(self.left_frame)
			tooltip_window.wm_overrideredirect(True)  # Entferne Fensterrahmen
			tooltip_window.attributes('-topmost', True)  # Halte den Tooltip im Vordergrund

			# Berechne die Position des Tooltips basierend auf der Mausposition
			x, y = widget.winfo_rootx(), widget.winfo_rooty()  # Mausposition relativ zum Eingabefeld
			tooltip_window.geometry(f'+{x + 50}+{y}')  # Positionieren Sie den Tooltip nahe dem Eingabefeld

			# Tooltip-Inhalt
			label = tk.Label(
				tooltip_window,
				text=text,
				font=('Arial', 12),
				bg='lightyellow',
				fg='black',
				relief='solid',
				bd=1,
				padx=5,
				pady=3,
				justify='left',
			)
			label.pack()

		# Funktion zum Verstecken des Tooltips
		def hide_tooltip(event):
			nonlocal tooltip_window
			if tooltip_window is not None:
				tooltip_window.destroy()  # Entferne das Tooltip-Fenster
				tooltip_window = None

		# Binde die Maus-Events an das Eingabefeld
		widget.bind('<Enter>', show_tooltip)  # Tooltip anzeigen, wenn Maus das Eingabefeld betritt
		widget.bind('<Leave>', hide_tooltip)  # Tooltip verstecken, wenn Maus das Eingabefeld verlässt


	def update_scrollregion(self, canvas, event=None):
		"""Aktualisiert die Scrollregion des Canvas basierend auf dem gesamten Inhalt."""
		
		# Berechne die Bounding-Box des Canvas-Inhalts
		bbox = canvas.bbox('all')
		if bbox:
			# Bounding-Box-Werte extrahieren
			x1, y1, x2, y2 = bbox
			y1 += 4  # Etwas Platz oben entfernen
			y2 -= 4  # Etwas Platz unten entfernen
			# Konfiguriere die Scrollregion des Canvas
			canvas.config(scrollregion=(x1, y1, x2, y2))


	def open_plotWindow(self):
		"""_summary_
			Öffnet ein neues Fenster mit Tabs, in denen die Plots angezeigt werden.
		"""
		# Überprüfen, ob das Fenster bereits existiert und sichtbar ist
		if hasattr(self, 'plotWindow') and self.plotWindow.winfo_exists():
			self.plotWindow.lift()  # Bringt das vorhandene Fenster in den Vordergrund
			return
		
		# Neues Tkinter-Fenster erstellen
		self.plotWindow = tk.Toplevel()
		self.plotWindow.title('Plots')

		# Fenster zentrieren
		window_width = 1000  # Beispielbreite
		window_height = 650  # Beispielhöhe
		screen_width = self.plotWindow.winfo_screenwidth()
		screen_height = self.plotWindow.winfo_screenheight()
		x = int((screen_width / 2) - (window_width / 2))
		y = int((screen_height / 2) - (window_height / 2))

		# Größe und Position des Fensters festlegen
		self.plotWindow.geometry(f'{window_width}x{window_height}+{x}+{y}')

		self.create_plotTabs()
		

	def create_plotTabs(self):
		# Notebook (Tabs) erstellen
		self.plot_tabs = ttk.Notebook(self.plotWindow)
		diagram = Diagrams(self.grid)
		# Tab 1: Pflanzen - Energy
		self.plants_energy_plot_tab = tk.Frame(self.plot_tabs)
		self.plot_tabs.add(self.plants_energy_plot_tab, text='Plants-Energy')
		diagram.dataPlotter(
			root=self.plants_energy_plot_tab,
			data_dict=self.grid.plantData,
			simLength=self.sim.simLength,
			measure='energy',
			title='Energy by Plant Type Over Time',
			ylabel='Energy'
		)

		# Tab 2: Pflanzen - Count
		self.plants_count_plot_tab = tk.Frame(self.plot_tabs)
		self.plot_tabs.add(self.plants_count_plot_tab, text='Plants-Count')
		diagram.dataPlotter(
			root=self.plants_count_plot_tab,
			data_dict=self.grid.plantData,
			simLength=self.sim.simLength,
			measure='count',
			title='Number by Plant Types Over Time',
			ylabel='Count'
		)

		# Tab 3: Feinde - Size
		self.enemies_size_plot_tab = tk.Frame(self.plot_tabs)
		self.plot_tabs.add(self.enemies_size_plot_tab, text='Enemies-Size')
		diagram.dataPlotter(
			root=self.enemies_size_plot_tab,
			data_dict=self.grid.EnemyData,
			simLength=self.sim.simLength,
			measure='size',
			title='Clustersize by Enemy Type Over Time',
			ylabel='Size'
		)

		# Tab 4: Feinde - Count
		self.enemies_count_plot_tab = tk.Frame(self.plot_tabs)
		self.plot_tabs.add(self.enemies_count_plot_tab, text='Enemies-Count')
		diagram.dataPlotter(
			root=self.enemies_count_plot_tab,
			data_dict=self.grid.EnemyData,
			simLength=self.sim.simLength,
			measure='count',
			title='Number by Enemy Types Over Time',
			ylabel='Count'
		)

		# Tabs anzeigen
		self.plot_tabs.pack(fill='both', expand=True)
	

	def open_breakupWindow(self):
		if hasattr(self, 'breakupWindow') and self.breakupWindow.winfo_exists():
			self.breakupWindow.deiconify()  # Fenster wieder anzeigen, falls es schon existiert
			return
		
		self.breakupWindow = tk.Toplevel()
		self.breakupWindow.title('Breakups')
		x = int(self.breakupWindow.winfo_screenwidth() / 2 - 400 / 2)
		y = int(self.breakupWindow.winfo_screenheight() / 2 - 200 / 2)
		# Setzen der Fenstergröße und Position
		self.breakupWindow.geometry(f'300x200+{x}+{y}')

		self.breakupWindow.grid_columnconfigure(0, weight=0)  # Kein Platz für Spalte 0
		self.breakupWindow.grid_columnconfigure(1, weight=1)  # Platz für Labels

		self.create_breakupWindow()


	def create_breakupWindow(self):
		tk.Label(self.breakupWindow, text='Maximum Sim-Steps:').grid(row=1, column=1, padx=2, pady=2, sticky='w')
		self.maxStepsBreakup_entry = tk.Entry(self.breakupWindow, width=10)
		self.maxStepsBreakup_entry.grid(row=1, column=2, padx=2, pady=2, sticky='w')

		tk.Label(self.breakupWindow, text='Death of plant:').grid(row=2, column=1, padx=2, pady=2, sticky='w')
		self.plantBreakup_entry = tk.Entry(self.breakupWindow, width=10)
		self.plantBreakup_entry.grid(row=2, column=2, padx=2, pady=2, sticky='w')

		tk.Label(self.breakupWindow, text='Death of enemy:').grid(row=3, column=1, padx=2, pady=2, sticky='w')
		self.enemyBreakup_entry = tk.Entry(self.breakupWindow, width=10)
		self.enemyBreakup_entry.grid(row=3, column=2, padx=2, pady=2, sticky='w')

		tk.Label(self.breakupWindow, text='Maximum plant energy:').grid(row=4, column=1, padx=2, pady=2, sticky='w')
		self.maxEnergyBreakup_entry = tk.Entry(self.breakupWindow, width=10)
		self.maxEnergyBreakup_entry.grid(row=4, column=2, padx=2, pady=2, sticky='w')

		tk.Label(self.breakupWindow, text='Maximum number of enemies:').grid(row=5, column=1, padx=2, pady=2, sticky='w')
		self.maxEnemiesBreakup_entry = tk.Entry(self.breakupWindow, width=10)
		self.maxEnemiesBreakup_entry.grid(row=5, column=2, padx=2, pady=2, sticky='w')

		tk.Button(self.breakupWindow, text='Apply', command=self.set_breakupsManuelly).grid(row=6, column=2, padx=2, pady=2, sticky='e')


	def set_breakupsAuto(self):
		self.maxSteps = None
		self.plant_death = None
		self.enemy_death = None
		self.max_plant_energy = None
		self.max_enemies_num = None


	def set_breakupsManuelly(self):
		try:
			self.maxSteps = int(self.maxStepsBreakup_entry.get()) if self.maxStepsBreakup_entry.get() else None
		except ValueError:
			messagebox.showerror('Invalid input', 'Please enter a valid number for maximum Sim-Steps')
			return
		
		self.plant_death = self.plantBreakup_entry.get()
		# Überprüfen, ob plant_death die Form 'p' gefolgt von 1 bis 16 hat
		if self.plant_death:
			if not re.fullmatch(r'p(1[0-6]|[1-9])', self.plant_death):
				messagebox.showerror('Invalid input', 'Please enter a valid format for plant death (e.g., p1 to p16)')
				return
		else:
			self.plant_death = None
		
		self.enemy_death = self.enemyBreakup_entry.get()
		# Überprüfen, ob enemy_death die Form 'e' gefolgt von 1 bis 15 hat
		if self.enemy_death:
			if not re.fullmatch(r'e(1[0-5]|[1-9])', self.enemy_death):
				messagebox.showerror('Invalid input', 'Please enter a valid format for enemy death (e.g., e1 to e15)')
				return
		else:
			self.enemy_death = None

		try:
			self.max_plant_energy = int(self.maxEnergyBreakup_entry.get()) if self.maxEnergyBreakup_entry.get() else None
		except ValueError:
			messagebox.showerror('Invalid input', 'Please enter a valid number for maximum energy')
			return
		
		try:
			self.max_enemies_num = int(self.maxEnemiesBreakup_entry.get()) if self.maxEnemiesBreakup_entry.get() else None
		except ValueError:
			messagebox.showerror('Invalid input', 'Please enter a valid number for maximum enemies number')
			return
		
		# Fenster verstecken
		self.breakupWindow.withdraw()
		print(self.maxSteps, self.plant_death, self.enemy_death, self.max_plant_energy, self.max_enemies_num)


	def create_gridFrame(self, width, height):
		self.grid_frame = tk.Frame(self.right_frame, bg='white')
		self.grid_frame.pack_propagate(False)  # Verhindert, dass der Frame seine Größe an Inhalte anpasst
		self.grid_frame.pack(fill='both', expand=True)

		# Canvas für das Grid
		self.gridCanvas = tk.Canvas(self.grid_frame, bg='white', bd=0, relief='solid')
		self.gridCanvas.pack(fill='both', expand=True)

		# Registriere den Event-Handler für Mausklicks
		self.gridCanvas.bind('<Button-1>', self.on_GridClick_player)
		self.gridCanvas.bind('<Button-2>', self.on_GridRightClick)  # Rechtsklick registrieren

		# Bereinige die Canvas vor dem Zeichnen
		self.gridCanvas.delete('all')

		# Aktualisiere die Canvas-Größe
		self.gridCanvas.update()
		canvas_width = self.gridCanvas.winfo_width()
		canvas_height = self.gridCanvas.winfo_height()

		# Weitere Logik, um das Grid zu zeichnen
		self.calculateSquareSize(width, height, canvas_width, canvas_height)


	def calculateSquareSize(self, width, height, canvas_width, canvas_height):
		# Berechne die maximale Quadratgröße, aber behalte die Höhe unverändert
		if width > 0 and height > 0:
			square_height = int(canvas_height / height)  # Höhe bleibt unverändert
			square_width = int(canvas_width / width)    # Breite passt sich der Canvas-Breite an
			
			# Berechne die tatsächliche Breite und Höhe des Grids
			grid_width = square_width * width
			grid_height = square_height * height
			
			# Zentriere das Grid, indem du Offsets berechnest
			x_offset = (canvas_width - grid_width) / 2
			y_offset = (canvas_height - grid_height) / 2

		self.drawGrid(width, height, x_offset, y_offset, square_width, square_height)


	def drawGrid(self, width, height, x_offset, y_offset, square_width, square_height):
		# Zeichne die Quadrate
		self.squares = {}
		for i in range(height):
			for j in range(width):
				# Koordinaten für das äußere Rechteck
				outer_x1 = x_offset + i * square_width
				outer_y1 = y_offset + j * square_height
				outer_x2 = outer_x1 + square_width
				outer_y2 = outer_y1 + square_height

				# Zeichne das äußere Rechteck
				outer_square_id = self.gridCanvas.create_rectangle(
					outer_x1, outer_y1, outer_x2, outer_y2,
					outline='black', fill='white', width=1
				)

				# Koordinaten für das innere Rechteck (leicht verkleinert)
				margin = min(square_width, square_height) * 0.08  # 10% der kleineren Dimension

				inner_x1 = outer_x1 + margin+2
				inner_y1 = outer_y1 + margin+2
				inner_x2 = outer_x2 - margin
				inner_y2 = outer_y2 - margin

				# Zeichne das innere Rechteck
				inner_square_id = self.gridCanvas.create_rectangle(
					inner_x1, inner_y1, inner_x2, inner_y2,
					outline='', fill='white', width=1
				)

				# Speichere die IDs des inneren und äußeren Rechtecks
				self.squares[(i, j)] = {
					'outer': outer_square_id,
					'inner': inner_square_id
				}


	def on_GridClick_player(self, event):
		# Ermittle die angeklickte Zelle
		clicked_item = self.gridCanvas.find_closest(event.x, event.y)
		if clicked_item:
			item_id = clicked_item[0]

			# Finde die (x, y)-Koordinaten der angeklickten Zelle
			clicked_position = None
			for position, ids in self.squares.items():
				if ids['inner'] == item_id:  # Überprüfen, ob der Klick das innere Rechteck getroffen hat
					clicked_position = position
					break

			if clicked_position is None:
				print(f'Zelle mit innerer ID {item_id} nicht gefunden.')
				return

			# Prüfe, ob eine Pflanze oder ein Feind ausgewählt ist
			selected_index = self.selectedItem.get()
			if selected_index == -1:
				# Keine Auswahl getroffen
				return

			# Überprüfen, ob eine Pflanze oder ein Feind ausgewählt wurde
			if selected_index < 16:  # Pflanzen haben Werte von 0 bis 15
				self.plantPlacer(clicked_position, selected_index)
			else:  # Feinde haben Werte ab 16
				self.enemyClusterPlacer(clicked_position, selected_index)



	def plantPlacer(self, position, selected_index):
		"""
		Platziert eine Pflanze auf dem Grid an den gegebenen Koordinaten (x, y).
		Zeigt die Energie der Pflanze oben innerhalb der Zelle an.
		"""
		square_ids = self.squares.get(position)
		
		if square_ids:  # Sicherstellen, dass die Position im Grid existiert
			inner_id = square_ids['inner']  # Nur den inneren Bereich ansprechen
			
			# Hole die Eingabewerte für die Pflanze
			plant_entries = self.plant_entries[selected_index]
			
			# Überprüfe, ob alle Eingabewerte gültig sind (nicht leer und im richtigen Format)
			try:
				init_energy, growth_rate, min_energy, repro_interval, off_energy, min_dist, max_dist = self.get_plantInputs(plant_entries)
			except ValueError:
				# Falls ein Wert ungültig ist, gebe eine Fehlermeldung aus
				self.error_plants.config(text='Error: All input values ​​must be valid numbers!', fg='red')
				return  # Beende die Funktion ohne die Pflanze hinzuzufügen

			# Überprüfe, ob alle Eingabewerte nicht leer sind (außer repro_interval)
			if not all([init_energy, growth_rate, min_energy, min_dist, max_dist]):
				self.error_plants.config(text='Error: All fields must be filled in!', fg='red')
				return  # Beende die Funktion ohne die Pflanze hinzuzufügen

			# Färbe den **inneren** Bereich der angeklickten Zelle
			plant_color = self.PLANT_COLORS[selected_index]
			self.gridCanvas.itemconfig(inner_id, fill=plant_color)
			
			# Erzeuge und füge Pflanze hinzu
			plant = self.create_add_plant(selected_index, position, init_energy, growth_rate, min_energy, repro_interval, off_energy, min_dist, max_dist, plant_color)
			self.plantDetails(plant, inner_id)
	

	def get_plantInputs(self, plant_entries):
		init_energy = int(plant_entries['initEnergy'].get())
		growth_rate = int(plant_entries['growthRate'].get())
		min_energy = int(plant_entries['minEnergy'].get())
				
		# Überprüfe, ob repro_interval leer ist, falls ja, setze auf 0
		repro_interval_str = plant_entries['reproInterval'].get()
		if repro_interval_str == '':
			repro_interval = 0  # Setze auf 0, wenn leer
		else:
			repro_interval = int(repro_interval_str)

		off_energy = int(plant_entries['offspring'].get())
				
		min_dist = int(plant_entries['minDist'].get())
		max_dist = int(plant_entries['maxDist'].get())
		if max_dist < min_dist:
			max_dist = min_dist + 1
		else:
			pass

		return init_energy, growth_rate, min_energy, repro_interval, off_energy, min_dist, max_dist
	

	def create_add_plant(self, selected_index, position, init_energy, growth_rate, min_energy, repro_interval, off_energy, min_dist, max_dist, plant_color):
		# Überprüfen, ob auf der Position bereits eine Pflanze existiert
		existing_plant = self.grid.getPlantAt(position)
		
		if existing_plant:
			# Wenn eine Pflanze vorhanden ist, entfernen sie
			self.grid.removePlant(existing_plant)  # Entferne die alte Pflanze
			print(f'Pflanze auf {position} entfernt und durch neue ersetzt.')

		# Pflanze instanziieren
		plant = Plant(
			name=f'p{selected_index + 1}',
			initEnergy=init_energy,
			growthRateEnergy=growth_rate,
			minEnergy=min_energy,
			reproductionInterval=repro_interval,
			offspringEnergy=off_energy,
			minDist=min_dist,
			maxDist=max_dist,
			position=position,
			grid=self.grid,
			color=plant_color)

		self.error_plants.config(text='')  # Fehlerbehandlung zurücksetzen

		# Pflanze zur Grid hinzufügen
		if plant not in self.grid.plants:
			self.grid.addPlant(plant)
			
			# Hole die Square-IDs für diese Position (inner und outer)
			square_ids = self.squares.get(plant.position)
			
			if square_ids:
				inner_id = square_ids['inner']  # ID für den inneren Bereich
				self.plant_at_position[inner_id] = plant
			else:
				print(f'Fehler: Keine gültigen Square-IDs für Position {plant.position}')

		else:
			pass
		return plant


	
	def plantDetails(self, plant, square_id):
		"""
		Zeigt die Energie der Pflanze als Tooltip an, wenn die Maus über die Zelle bewegt wird.
		"""
		tooltip_window = None  # Variable für das Tooltip-Fenster

		# Funktion zum Anzeigen des Tooltips
		def show_tooltip(event):
			nonlocal tooltip_window

			if tooltip_window is not None:
				return  # Verhindert mehrfaches Erstellen von Tooltips

			# Berechne die Energie der Pflanze dynamisch
			energy_percentage = int((plant.currEnergy / plant.initEnergy) * 100)
			tooltip_text = f'Name: {plant.name}\nEnergy: {energy_percentage}%\nPosition: {plant.position}'

			# Erstelle ein neues Fenster für den Tooltip
			tooltip_window = tk.Toplevel(self.gridCanvas)
			tooltip_window.wm_overrideredirect(True)  # Entferne Fensterrahmen
			tooltip_window.attributes('-topmost', True)  # Halte den Tooltip im Vordergrund

			# Setze die Tooltip-Position
			x, y = self.gridCanvas.winfo_pointerxy()  # Mausposition relativ zum Bildschirm
			tooltip_window.geometry(f'+{x + 10}+{y + 10}')

			# Tooltip-Inhalt
			label = tk.Label(
				tooltip_window,
				text=tooltip_text,
				font=('Arial', 12),
				bg='white',
				fg='black',
				relief='solid',
				bd=1,
				padx=5,
				pady=3,
			)
			label.pack()

		# Funktion zum Verstecken des Tooltips
		def hide_tooltip(event):
			nonlocal tooltip_window
			if tooltip_window is not None:
				tooltip_window.destroy()  # Entferne das Tooltip-Fenster
				tooltip_window = None

		# Binde die Maus-Events an das Zellen-Item
		self.gridCanvas.tag_bind(square_id, '<Enter>', show_tooltip)  # Tooltip anzeigen, wenn Maus die Zelle betritt
		self.gridCanvas.tag_bind(square_id, '<Leave>', hide_tooltip)  # Tooltip verstecken, wenn Maus die Zelle verlässt


	def enemyClusterPlacer(self, clicked_position, selected_index):
		"""
		Platziert einen Feind-Cluster auf dem Grid an den gegebenen Koordinaten (x, y).
		"""
		square_ids = self.squares.get(clicked_position)

		if square_ids:
			# Hole die ID des äußeren Bereichs (outer) - für Feind-Visualisierung
			inner_id = square_ids['inner']
			# Übersetze den Index
			actual_index = self.enemy_index_mapping[selected_index]
			enemy_entries = self.enemy_entries[actual_index]

			# Überprüfe, ob alle Eingabewerte gültig sind
			try:
				clusterSize, speed, eatSpeed, eatVictory = self.get_enemyInputs(enemy_entries)
			except ValueError:
				# Falls ein Wert ungültig ist, gebe eine Fehlermeldung aus
				self.error_enemies.config(text='Error: All input values must be valid numbers!', fg='red')
				return  # Beende die Funktion ohne den Feind hinzuzufügen

			# Überprüfe, ob alle Eingabewerte nicht leer sind
			if not all([clusterSize, speed, eatSpeed, eatVictory]):
				self.error_enemies.config(text='Error: All fields must be filled in!', fg='red')
				return  # Beende die Funktion ohne den Feind hinzuzufügen

			# Färbe die angeklickte Zelle
			eCluster = self.create_add_cluster(selected_index, clicked_position, clusterSize, speed, eatSpeed, eatVictory)
			self.clusterMarker(clicked_position, selected_index, eCluster)



	def get_enemyInputs(self, enemy_entries):
		"""
		Holt und validiert die Eingabewerte für einen Feind-Cluster.
		"""
		# Extrahiere die Eingabewerte
		clusterSize = int(enemy_entries['clusterSize'].get())
		speed = int(enemy_entries['speed'].get())
		eatSpeed = int(enemy_entries['eatSpeed'].get())
		eatVictory = int(enemy_entries['eatVictory'].get())

		# Rückgabe der validierten Werte
		return clusterSize, speed, eatSpeed, eatVictory


	def create_add_cluster(self, selected_index, clicked_position, clusterSize, speed, eatSpeed, eatVictory):
		enemy = Enemy(name=f'e{selected_index - 15}', symbol=f'E{selected_index - 15}')

		cluster = EnemyCluster(enemy=enemy,
						 num=clusterSize,
						 position=clicked_position,
						 grid=self.grid,
						 speed=speed,
						 eatingSpeed=eatSpeed,
						 eatVictory=eatVictory)

		self.error_enemies.config(text='')

		if cluster not in self.grid.enemies:
			self.grid.addEnemies(cluster)
		else:
			pass
		return cluster
	

	def clusterMarker(self, clicked_position, selected_index, cluster):
		"""Platziert einen Marker für den Feind auf dem Canvas als kleinen Kreis."""

		# Berechne die Pixelposition aus den Gridkoordinaten
		x_pos, y_pos = self.get_cellPosition(clicked_position)

		circle_id = self.create_clusterCircle(x_pos, y_pos)  # Feindinformationen speichern

		# Speichere die Marker-ID im Cluster
		cluster.circle_id = circle_id

		# Feindinformationen für diese Position speichern  
		if clicked_position not in self.enemies_at_positions:
			self.enemies_at_positions[clicked_position] = []  # Initialisiere Liste für diese Position, falls sie noch nicht existiert

		# Füge die Feindinformationen zur Liste hinzu
		self.enemies_at_positions[clicked_position].append(cluster)

		# Füge Tooltip hinzu
		self.enemyDetails(circle_id, clicked_position)
		#print(f'Feind {cluster.enemy.name} mit Clustergröße {cluster.num} platziert auf: {clicked_position}')


	def get_cellPosition(self, position):
		"""
		Berechnet die Position der inneren Zelle basierend auf den Koordinaten und berücksichtigt Scroll-Offsets.
		"""
		# Hole die Square-IDs für die gegebene Position
		square_ids = self.squares.get(position)  # Erhalte die IDs (inner/outer) von den Koordinaten
		if square_ids is None:
			print(f'Fehler: Keine Zelle mit den Koordinaten {position} gefunden.')
			return None  # Zelle nicht gefunden

		# Verwende die ID des inneren Bereichs ('inner')
		inner_id = square_ids.get('inner')
		if inner_id is None:
			print(f'Fehler: Keine innere Zelle für die Koordinaten {position} gefunden.')
			return None  # Innerer Bereich nicht gefunden

		# Hole die Bounding Box der inneren Zelle
		bbox = self.gridCanvas.bbox(inner_id)
		if bbox is None:
			print(f'Fehler: Keine Bounding Box für die Zelle mit item_id {inner_id} gefunden.')
			return None  # Bounding Box nicht gefunden

		# Berechne die zentrale Position der inneren Zelle
		cell_width = bbox[2] - bbox[0]
		cell_height = bbox[3] - bbox[1]
		x_pos = bbox[0] + cell_width / 2
		y_pos = bbox[1] + cell_height / 2

		# Positionen für Feinde in der Zelle berücksichtigen
		if not hasattr(self, 'enemy_positions'):
			self.enemy_positions = {}

		if position not in self.enemy_positions:
			self.enemy_positions[position] = 0

		current_enemy_count = self.enemy_positions[position]
		y_pos += current_enemy_count * 15  # Verschiebe die Y-Position für mehrere Feinde in derselben Zelle

		return x_pos, y_pos

	
	def create_clusterCircle(self, x_pos, y_pos, fill_color='navy'): 
		""" Zeichnet einen kleinen Kreis, um den Feind auf dem Canvas darzustellen. """

		circle_radius = 2.5  # Kleinere Kreisgröße für den Feind 
		
		# Berechne die Koordinaten für den Kreis (Bounding Box: (left, top, right, bottom)) 
		left = x_pos - circle_radius 
		top = y_pos - circle_radius 
		right = x_pos + circle_radius 
		bottom = y_pos + circle_radius # Zeichne den Kreis 
		circle_id = self.gridCanvas.create_oval(left, top, right, bottom, fill=fill_color, outline='black') 
		return circle_id
	

	def enemyDetails(self, circle_id, position):
		"""
		Fügt Tooltip-Logik für einen Canvas-Text hinzu, der auch außerhalb des Hauptfensters sichtbar ist.
		"""
		tooltip_window = None  # Variable für das Tooltip-Fenster

		# Funktion zum Anzeigen des Tooltips
		def show_tooltip(event):
			nonlocal tooltip_window

			if tooltip_window is not None:
				return  # Verhindert mehrfaches Erstellen des Tooltips

			# Sammle Informationen zu allen Feinden an dieser Position
			enemies_at_pos = self.enemies_at_positions.get(position, [])
			tooltip_text = '\n'.join(f'{ec.enemy.name}: Size {int(ec.num)}, Intox-State {ec.intoxicated}' for ec in enemies_at_pos)

			# Erstelle ein neues Fenster für den Tooltip
			tooltip_window = tk.Toplevel(self.gridCanvas)
			tooltip_window.wm_overrideredirect(True)  # Entferne Fensterrahmen
			tooltip_window.attributes('-topmost', True)  # Halte den Tooltip im Vordergrund

			# Positioniere das Tooltip-Fenster
			x, y = self.gridCanvas.winfo_pointerxy()  # Mausposition relativ zum Bildschirm
			tooltip_window.geometry(f'+{x + 10}+{y + 10}')

			# Tooltip-Inhalt
			label = tk.Label(
				tooltip_window,
				text=tooltip_text,
				font=('Arial', 12),
				bg='white',
				fg='black',
				relief='solid',
				bd=1,
				padx=5,
				pady=3,
			)
			label.pack()

		# Funktion zum Verstecken des Tooltips
		def hide_tooltip(event):
			nonlocal tooltip_window
			if tooltip_window is not None:
				tooltip_window.destroy()  # Entferne das Tooltip-Fenster
				tooltip_window = None

		# Binde die Maus-Events an das Canvas-Element
		self.gridCanvas.tag_bind(circle_id, '<Enter>', show_tooltip)  # Tooltip anzeigen, wenn Maus das Element betritt
		self.gridCanvas.tag_bind(circle_id, '<Leave>', hide_tooltip)  # Tooltip verstecken, wenn Maus das Element verlässt


	def on_GridRightClick(self, event):
		"""
		Behandelt Rechtsklicks auf das Grid und zeigt ein Popup an, wenn der innere Bereich einer Zelle geklickt wird.
		"""
		# Ermittle das angeklickte Canvas-Element
		clicked_item = self.gridCanvas.find_closest(event.x, event.y)
		if clicked_item:
			item_id = clicked_item[0]

			# Finde die (x, y)-Koordinaten der angeklickten Zelle basierend auf der inner-ID
			clicked_position = None
			for position, ids in self.squares.items():
				inner_id = ids.get('inner')  # Hole die ID des inneren Bereichs
				if inner_id == item_id:  # Überprüfe, ob die geklickte ID mit der inner-ID übereinstimmt
					clicked_position = position
					break

			if clicked_position is None:
				print(f'Innerer Bereich der Zelle mit ID {item_id} nicht gefunden.')
				return

			# Prüfe, ob eine Pflanze oder ein Feind ausgewählt ist
			selected_index = self.selectedItem.get()
			if selected_index == -1:
				# Keine Auswahl getroffen
				return

			# Überprüfe, ob an dieser Position eine Pflanze existiert
			plant = self.grid.getPlantAt(clicked_position)
			if plant:
				# Zeige das Popup nur, wenn eine Pflanze existiert
				self.show_popup(clicked_position, event)
			else:
				print(f'Keine Pflanze an Position {clicked_position}.')


	def show_popup(self, position, event):
		# Öffnet ein Popup-Fenster, das die benachbarten Felder anzeigt
		popup = tk.Toplevel(self.grid_frame)

		# Berechne die Position des Popups basierend auf den Mauskoordinaten
		x = event.x_root
		y = event.y_root
		
		# Setze die Position des Popups relativ zur Mausposition
		popup.geometry(f'+{x+10}+{y+10}')  # Füge einen kleinen Abstand hinzu, damit es nicht direkt unter der Maus erscheint

		# Erhalte die benachbarten Felder mit Pflanzen für die angeklickte Zelle
		neighbors = self.get_neighbors(position)

		# Wenn benachbarte Felder mit Pflanzen existieren, füge einen Checkbutton hinzu
		if neighbors:
			tk.Label(popup, text=f'Neighbors of {position}:').pack()

			# Dictionary, um die Checkbutton-Status zu speichern
			self.checkbutton_neighbors_vars = {}
			plant = self.grid.getPlantAt(position)

			# Erstelle für jedes benachbarte Feld einen Checkbutton
			for neighbor_position in neighbors:
				neighbor_plant = self.grid.getPlantAt(neighbor_position)  # Überprüfe, ob eine Pflanze an diesem Nachbarfeld existiert
				if neighbor_plant:
					# Initialisiere BooleanVar basierend auf dem aktuellen Verbindungsstatus
					is_connected = self.plant_connections.get((plant, neighbor_plant), False)
					var = tk.BooleanVar(value=is_connected)
					self.checkbutton_neighbors_vars[neighbor_plant] = var  # Speichere die Variable für jede benachbarte Pflanze
					
					# Erstelle eine Callback-Funktion für jeden Checkbutton
					def toggle_connection(n_plant, n_var):
						if n_var.get():
							# Verbindung herstellen
							print(f'Verbindung hergestellt: {plant.name} <-> {n_plant.name}')
							self.connect_plants(plant, n_plant)
						else:
							# Verbindung entfernen
							print(f'Verbindung entfernt: {plant.name} <-> {n_plant.name}')
							self.disconnect_plants(plant, n_plant)

					# Erstelle einen Checkbutton und binde die spezifische Nachbarpflanze
					tk.Checkbutton(
						popup,
						text=f'{plant.name} connection to {neighbor_plant.name}',
						variable=var,
						command=lambda n=neighbor_plant, v=var: toggle_connection(n, v)
					).pack()

		else:
			# Falls keine benachbarten Felder existieren
			tk.Label(popup, text=f'No neighbors at {position}').pack()


	def get_neighbors(self, position):
		"""
		Diese Methode gibt die benachbarten Felder zurück, auf denen eine Pflanze vorhanden ist.
		Überprüft alle benachbarten Felder (oben, unten, links, rechts).
		"""
		
		x, y = position
		neighbors = [
			(x - 1, y), # oben
			(x, y - 1), # links
			(x, y + 1), # rechts
			(x + 1, y)  # unten
		]
		
		valid_neighbors = []
		
		for neighbor in neighbors:
			# Stelle sicher, dass der Nachbar innerhalb der Grenzen des Grids liegt
			if 0 <= neighbor[0] < int(self.grid_size_entry.get()) and 0 <= neighbor[1] < int(self.grid_size_entry.get()):
				# Überprüfe, ob an dieser Position eine Pflanze existiert
				plant = self.grid.getPlantAt(neighbor)  # Methode getPlantAt überprüft, ob dort eine Pflanze ist
				if plant:  # Wenn eine Pflanze gefunden wurde
					valid_neighbors.append(neighbor)
		
		return valid_neighbors


	def connect_plants(self, plant, neighbor):
		"""
		Diese Methode erstellt eine Symbiose-Verbindung zwischen zwei Pflanzen.
		"""
		# Verbindung erstellen und in der Datenstruktur speichern
		connection = SymbioticConnection(plant, neighbor)
		connection.createConnection()

		# Speichere die Verbindung in beiden Richtungen
		self.plant_connections[(plant, neighbor)] = True
		self.plant_connections[(neighbor, plant)] = True

		print(f'Verbindung gespeichert: {plant.name} <-> {neighbor.name}')
		self.create_connectionLine(plant, neighbor)


	def disconnect_plants(self, plant, neighbor):
		"""
		Entfernt die Symbiose-Verbindung zwischen zwei Pflanzen.
		"""
		# Entferne die Verbindung aus dem Dictionary
		if (plant, neighbor) in self.plant_connections:
			del self.plant_connections[(plant, neighbor)]
		if (neighbor, plant) in self.plant_connections:
			del self.plant_connections[(neighbor, plant)]

		print(f'Verbindung entfernt: {plant.name} <-> {neighbor.name}')
		self.remove_connectionLine(plant, neighbor)


	def create_connectionLine(self, plant, neighbor):
		plant_center = self.get_cellPosition(plant.position)
		neighbor_center = self.get_cellPosition(neighbor.position)

		if plant_center is None or neighbor_center is None:
			print(f'Fehler: Ungültige Positionen für Pflanzen {plant.name} und {neighbor.name}')
			return

		# Ziehe eine Linie zwischen den Mittelpunkten der beiden Zellen
		line = self.gridCanvas.create_line(
			plant_center[0], plant_center[1], neighbor_center[0], neighbor_center[1],
			fill='purple', width=2  # Optional: Anpassung der Farbe und Breite der Linie
		)
		# Speichere die Linie, um sie später zu bearbeiten oder zu löschen
		self.grid_lines[(plant, neighbor)] = line


	def remove_connectionLine(self, plant, neighbor):
		# Entferne die Linie, falls sie existiert
		if (plant, neighbor) in self.grid_lines:
			line_id = self.grid_lines[(plant, neighbor)]  # Hole die Linien-ID
			self.gridCanvas.delete(line_id)  # Lösche die Linie von der Canvas
			del self.grid_lines[(plant, neighbor)]  # Lösche den Eintrag aus grid_lines
		elif (neighbor, plant) in self.grid_lines:
			line_id = self.grid_lines[(neighbor, plant)]  # Hole die Linien-ID
			self.gridCanvas.delete(line_id)  # Lösche die Linie von der Canvas
			del self.grid_lines[(neighbor, plant)]  # Lösche den Eintrag aus grid_lines


	def get_substanceInputs(self, substance_entries):
		substance_values = []
		idxs = []

		for index, entry_data in substance_entries.items():
			checkbox_var = entry_data['checkbox_var'].get()
			type_var = entry_data['type_var'].get()
			toxin_effect_var = entry_data['toxinEffect_var'].get()
			spread_type_var = entry_data['spreadType_var'].get()
			name = entry_data['subName'].get()
			producer = entry_data['producer'].get()
			receiver = entry_data['receiver'].get()
			trigger = entry_data['trigger'].get()
			prod_time = entry_data['prodTime'].get()
			send_speed = entry_data['sendSpeed'].get()
			energy_costs = entry_data['energyCosts'].get()
			after_effect_time = entry_data['aft'].get()
			eli_stren = entry_data['eliStrength'].get()
			# Alle Werte für eine Substanz als Tuple in der Liste speichern
			substance_values.append((checkbox_var, type_var, toxin_effect_var, spread_type_var, 
									name, producer, receiver, trigger, 
									prod_time, send_speed, energy_costs, after_effect_time, eli_stren))

			idxs.append(index)
		# Alle Werte nach dem Schleifenende zurückgeben
		return substance_values, idxs

	def validate_substanceInputs(self, substance_entries):

		substance_values = []
		idxs = []
		valid_substances = []
		errors = []
		try:
			substance_values, idxs = self.get_substanceInputs(substance_entries)
		except ValueError:
			# Falls ein Wert ungültig ist, gebe eine Fehlermeldung aus
			self.error_substances.config(text='Error: All input values ​​must be valid!', fg='red')
			return  # Beende die Funktion ohne die Substanz hinzuzufügen

		# Schleife über alle Substanzen in substance_values
		for i, values in zip(idxs, substance_values):
			checkbox_var, type_var, toxin_effect_var, spread_type_var, name, producer, receiver, trigger, prod_time, send_speed, energy_costs, after_effect_time, eli_stren = values

			# Nur wenn das Checkbox-Feld aktiviert ist
			if checkbox_var == 1:
				# Überprüfe Name
				if not name or re.fullmatch(r'\s*', name):  # Prüfen, ob der Name leer oder nur aus Leerzeichen besteht
					errors.append('Please enter a valid name!')
				
				# Überprüfe Producer
				producer_pattern = r'^(p[1-9]|p1[0-6])(\s*,\s*(p[1-9]|p1[0-6]))*$'
				if not producer or not re.fullmatch(producer_pattern, producer):
					errors.append('Producer must be in the format "p1, p2, ..., p16"!')

				# Duplikate im Producer entfernen
				producers_list = [prod.strip() for prod in producer.split(',')]  # Liste von Produzenten
				producers_set = set(producers_list)  # Duplikate entfernen
				if len(producers_list) != len(producers_set):  # Wenn Duplikate entfernt wurden
					producers_list = list(producers_set)  # Umwandeln in Liste ohne Duplikate
				producer = ', '.join(producers_list)  # Zurück in einen kommagetrennten String

				# Überprüfe Receiver
				receiver_pattern = r'^(p[1-9]|p1[0-6])(\s*,\s*(p[1-9]|p1[0-6]))*$'
				if self.substance_entries[i]['receiver'].cget('state') == 'normal':
					if not receiver or not re.fullmatch(receiver_pattern, receiver):
						errors.append('Receiver must be in the format "p1, p2, ..., p16"!')			

				# Duplikate im Receiver entfernen
				receivers_list = [rec.strip() for rec in receiver.split(',')]  # Liste von Empfängern
				receivers_set = set(receivers_list)  # Duplikate entfernen
				if len(receivers_list) != len(receivers_set):  # Wenn Duplikate entfernt wurden
					receivers_list = list(receivers_set)  # Umwandeln in Liste ohne Duplikate
				receiver = ', '.join(receivers_list)  # Zurück in einen kommagetrennten String

				# Überprüfe Trigger
				if type_var == 'Signal':
					trigger_pattern = r'^(e([1-9]|1[0-5]),\s*(\d+))(\s*;\s*e([1-9]|1[0-5]),\s*(\d+))*$'
					if not trigger or not re.fullmatch(trigger_pattern, trigger):
						errors.append('Trigger must follow the format "e1, 1; e2, 2"!')

					triggers_list = [block.strip() for block in trigger.split(';')]  # Aufteilen in Blöcke, durch Semikolons getrennt
					for i in range(len(triggers_list)):
						triggers_list[i] = ', '.join(
							dict.fromkeys([part.strip() for part in triggers_list[i].split(',')])
						)  # Entferne Duplikate, behalte Reihenfolge
					trigger = '; '.join(triggers_list)  # Setze den Trigger zurück als korrekt formatierten String
				
				if type_var == 'Toxin':
					trigger_pattern = r'^((\w+),\s*(e[1-9]|e1[0-5]),\s*\d+)(\s*;\s*(\w+),\s*(e[1-9]|e1[0-5]),\s*\d+)*$'
					if not trigger or not re.fullmatch(trigger_pattern, trigger):
						errors.append('Trigger must be in the format "signal-name, e1, 1; s2, e2, 2"!')

					# Duplikate im Trigger entfernen
					triggers_list = [tr.strip() for tr in trigger.split(';')]  # Liste von Trigger-Blöcken
					triggers_list = list(dict.fromkeys(triggers_list))  # Entferne Duplikate, behalte Reihenfolge
					trigger = '; '.join(triggers_list)  # Setze den Trigger zurück als korrekt formatierten String
				
				# Überprüfe prod_time
				if not prod_time or not prod_time.isdigit():  # Prüft, ob es eine Zahl ist
					errors.append('prod time must be a valid number!')

				# Überprüfe send_speed
				if self.substance_entries[i]['sendSpeed'].cget('state') == 'normal':
					if not send_speed or not send_speed.isdigit():
						errors.append('send speed must be a valid number!')

				# Überprüfe energy_costs
				if self.substance_entries[i]['energyCosts'].cget('state') == 'normal':
					if not energy_costs or not energy_costs.isdigit():
						errors.append('energy costs must be a valid number!')

				# Überprüfe after_effect_time
				if self.substance_entries[i]['aft'].cget('state') == 'normal':
					if not after_effect_time or not after_effect_time.isdigit():
						errors.append('after effect time must be a valid number!')
				
				if self.substance_entries[i]['eliStrength'].cget('state') == 'normal':
					if not eli_stren or not eli_stren.isdigit():
						errors.append('elimination strength must be a valid number!')

				# Wenn keine Fehler, füge die Substanz zu valid_substances hinzu
				if not errors:
					valid_substances.append((checkbox_var, type_var, toxin_effect_var, spread_type_var, name, producer, receiver, trigger, prod_time, send_speed, energy_costs, after_effect_time, eli_stren))
					self.valid_substances_set = set(valid_substances)
				else:
					continue  # Wenn checkbox_var nicht 1 ist, überspringe die Substanz

		 # Wenn Fehler gefunden wurden, zeige sie an und gib False zurück
		if errors:
			for error in errors:
				messagebox.showerror('Invalid input', error)
			return False
		
		return True  # Rückgabewert True, wenn keine Fehler gefunden wurden
	
	
	def create_add_substance(self):
		self.validate_substanceInputs(self.substance_entries)
		
		for substance_value in self.valid_substances_set:
			substance_type = substance_value[1]
			input_name = substance_value[4]
			input_producer = substance_value[5]
			input_trigger = substance_value[7]
			input_prodTime = substance_value[8]

			sub = Substance(name=input_name, type=substance_type.lower())

			if  substance_type == 'Signal':
				input_spreadType = substance_value[3]
				input_receiver = substance_value[6]
				input_sendSpeed = substance_value[9]
				input_energyCost = substance_value[10]
				input_afterEffectTime = substance_value[11]
				
				sig = self.create_signal(sub, input_producer, input_receiver, input_trigger, input_prodTime, input_spreadType, input_sendSpeed, input_energyCost, input_afterEffectTime)

				if not any(s.substance.name == sig.substance.name for s in self.grid.signals):
					self.grid.addSubstance(sig)

		# Verarbeitung der Toxine
		for substance_value in self.valid_substances_set:
			if substance_value[1] == 'Toxin':
				input_name = substance_value[4]
				input_producer = substance_value[5]
				input_trigger = substance_value[7]
				input_prodTime = substance_value[8]
				input_deadly = substance_value[2]
				input_energyCost = substance_value[10]
				input_eliStrength = substance_value[12]
				
				sub = Substance(name=input_name, type='toxin')
				tox = self.create_toxin(sub, input_producer, input_energyCost, input_trigger, input_prodTime, input_deadly, input_eliStrength)
				
				if not any(t.substance.name == tox.substance.name for t in self.grid.toxins):
					self.grid.addSubstance(tox)

	
	def create_signal(self, sub, input_producer, input_receiver, input_trigger, input_prodTime, input_spreadType, input_sendSpeed, input_energyCost, input_afterEffectTime):
		trigger_elements = input_trigger.split(';')
		emit_elements = input_producer.split(',') 
		receive_elements = input_receiver.split(',')

		trigger_list = [[part.strip() if i == 0 else int(part.strip()) for i, part in enumerate(elem.split(','))] for elem in trigger_elements]
		# Ersetze Strings in emit_list durch Objekte
		emit_list = [part.strip() for part in emit_elements]

		# Ersetze Strings in receive_list durch Objekte
		receive_list = [part.strip() for part in receive_elements]
		
		sig = Signal(substance=sub, 
				 		emit=emit_list,
						receive=receive_list,
						triggerCombination=trigger_list,
						prodTime=int(input_prodTime),
						spreadType=input_spreadType.lower(),
						sendingSpeed=int(input_sendSpeed),
						energyCosts=int(input_energyCost),
						afterEffectTime=int(input_afterEffectTime))

		return sig
	

	def create_toxin(self, sub, input_producer, input_energyCost, input_trigger, input_prodTime, input_deadly, input_eliStrength):
		trigger_elements = input_trigger.split(';')
		producer_elements = input_producer.split(',')

		# Extrahiere Enemy-Objekte aus der Liste der EnemyCluster
		all_enemies = [cluster.enemy for cluster in self.grid.enemies if isinstance(cluster, EnemyCluster)]

		trigger_list = [[part.strip() if i == 0 
							else part.strip() if i == 1
            				else int(part.strip()) for i, part in enumerate(elem.split(','))] 
							for elem in trigger_elements]
		
		producer_list = [part.strip() for elem in producer_elements for part in elem.split(',')]

		tox = Toxin(substance=sub,
						plantTransmitter=producer_list,
						energyCosts=int(input_energyCost),
						triggerCombination=trigger_list,
						prodTime=int(input_prodTime),
						deadly=bool(input_deadly),
						eliminationStrength=int(input_eliStrength))
		return tox
	

	def find_object_by_name(self, name, object_list):
		for obj in object_list:
			if isinstance(obj, EnemyCluster):
				if obj.enemy.name == name:
					return obj
			if isinstance(obj, Enemy):
				if obj.name == name:
					return obj
			if isinstance(obj, Plant):
				if obj.name == name:
					return obj
			if isinstance(obj, Signal):
				if obj.name == name:
					return obj
			else:
				return None  # Falls kein Objekt gefunden wird
	

	def start_simulation(self):
		# Starte die Simulation in einem separaten Thread
		sim_thread = threading.Thread(target=self.run_simulation)
		sim_thread.daemon = True  # Beendet den Thread automatisch, wenn das Hauptprogramm endet
		sim_thread.start()


	def run_simulation(self):
		self.sim = Simulation(self.grid)
		self.sim.getPlantData(0)
		self.sim.getEnemyData(0)
		count = 1
		if not self.validate_substanceInputs(self.substance_entries):
			self.error_substances.config(text='Please check substance inputs.', fg='red')
			return  # Beende die Funktion, falls die Validierung fehlschlägt

		self.create_add_substance()
		self.error_substances.config(text='')
		while True:
			# Abbruchbedingungen
			if count - 1 == self.maxSteps or \
			self.sim.noSpecificPlantBreak(self.plant_death) or \
			self.sim.noSpeceficEnemyBreak(self.enemy_death) or \
			self.sim.noEnemiesBreak() or \
			self.sim.noPlantsBreak() or \
			self.sim.upperGridEnergyBreak(self.max_plant_energy) or \
			self.sim.upperEnemyNumBreak(self.max_enemies_num):
				break

			# Pflanzenwachstum parallelisieren
			with ThreadPoolExecutor() as executor:
				executor.map(self.grow_plant_para, self.grid.plants)

			# Nachkommen verteilen (scatterSeed) parallelisieren
			# Hier wird der 'count' als Argument mitgegeben
			plants_with_index = [(i, plant) for i, plant in enumerate(self.grid.plants)]
			with ThreadPoolExecutor() as executor:
				executor.map(lambda plant_with_index: self.scatter_seed_para(plant_with_index, count), plants_with_index)

			old_positions = {ec: ec.position for ec in self.grid.enemies}
			self.grid.collectAndManageEnemies()
			new_positions = {ec: ec.position for ec in self.grid.enemies}

			self.remove_fieldColor()
			self.gridCanvas.after(10)

			old_new_positions = {ec: (old_positions[ec], new_positions[ec]) for ec in self.grid.enemies}
			self.remove_dead_cluster(old_new_positions)
			self.update_enemyMarker(old_new_positions)
			
			self.show_substance()
				
			self.sim.getPlantData(count)
			self.sim.getEnemyData(count)
			self.roundCount.config(text=f'{count}', bg='orange')
			count += 1
			self.gridCanvas.after(150)
		self.sim.simLength = count - 1
		self.roundCount.config(bg='green')


	def grow_plant_para(self, plant):
		plant.grow()


	def scatter_seed_para(self, plant_with_index, count):
		# Pflanze und deren Index extrahieren
		plant_index, plant = plant_with_index

		# Holen des Reproduktionsintervalls und der Offspring-Energie
		repro_interval = plant.reproductionInterval
		offspring_energy = plant.offspringEnergy

		# Prüfen, ob die Pflanze reproduktiv ist und das Intervall erreicht wurde
		if repro_interval == 0 or count % repro_interval != 0:
			return  # Kein Fenster wird erzeugt, wenn das Intervall nicht erfüllt ist

		# Anzahl der Nachkommen ermitteln (z. B. 1 bis 4, abhängig von der scatterSeed-Logik)
		num_offspring = random.randint(1, 4)

		# Positionen für die Nachkommen ermitteln
		offspring_positions = [plant.setOffspringPos() for _ in range(num_offspring)]
		offspring_positions = [pos for pos in offspring_positions if pos]  # Filtere ungültige Positionen

		# Zufällige Auswahl der Positionen für die Nachkommen
		random.shuffle(offspring_positions)  # Zufällige Reihenfolge der Positionen
		
		# Platzieren der Nachkommen auf den zufälligen Positionen
		for i in range(min(num_offspring, len(offspring_positions))):  # Falls es weniger Positionen gibt als Nachkommen
			offspring_position = offspring_positions[i]

			# Hier wird ein Nachkomme erzeugt
			offspring = Plant(
				name=plant.name,
				initEnergy=offspring_energy,  # Die Energie des Nachkommens
				growthRateEnergy=plant.growthRateEnergy,  # Die Wachstumsrate der Mutterpflanze
				minEnergy=plant.minEnergy,  # Mindestenergie der Mutterpflanze
				reproductionInterval=plant.reproductionInterval,  # Reproduktionsintervall der Mutterpflanze
				offspringEnergy=plant.offspringEnergy,  # Energie für Nachkommen
				minDist=plant.minDist,  # Mindestdistanz der Mutterpflanze
				maxDist=plant.maxDist,  # Maximale Distanz der Mutterpflanze
				position=offspring_position,  # Position des Nachkommens
				grid=plant.grid,  # Grid der Mutterpflanze
				color=plant.color,  # Farbe der Mutterpflanze
			)

			# Füge das Nachkommen zum Grid hinzu
			self.add_offspring_to_grid(offspring, offspring_position)
	

	def add_offspring_to_grid(self, offspring, offspring_position):
		"""
		Fügt das Nachkommen zum Grid hinzu und zeigt es auf der Canvas, wenn das Feld frei ist.
		Der Nachkomme wird auf den inneren Bereich des Feldes gesetzt.
		"""
		# Prüfe, ob das Feld bereits existiert (es sollte aufgrund von drawGrid existieren)
		if offspring_position in self.squares:
			# Hole die IDs der inneren und äußeren Rechtecke für diese Position
			square_ids = self.squares[offspring_position]
			inner_square_id = square_ids['inner']  # ID für den inneren Bereich
			outer_square_id = square_ids['outer']  # ID für den äußeren Bereich

			# Falls es eine Pflanze auf dieser Position gibt, entfernen wir diese, falls sie tot ist
			existing_plant = self.plant_at_position.get(offspring_position)
			if existing_plant and existing_plant.currEnergy < existing_plant.minEnergy:
				# Setze die Farbe des äußeren Bereichs zurück auf Weiß
				self.gridCanvas.itemconfig(outer_square_id, fill='white')
				self.gridCanvas.itemconfig(inner_square_id, fill='white')  # Setze auch den inneren Bereich auf Weiß
				del self.plant_at_position[offspring_position]  # Entferne die Pflanze aus der Position

			# Füge das Nachkommen zum Grid hinzu
			if offspring not in self.grid.plants:
				self.grid.addPlant(offspring)
				# print(f'Nachkomme {offspring.name} wurde dem Grid hinzugefügt.')

			# Aktualisiere die Canvas-Farbe des inneren Rechtecks und das Mapping
			self.gridCanvas.itemconfig(inner_square_id, fill=offspring.color)  # Ändere die Farbe des inneren Quadrats
			self.plant_at_position[offspring_position] = offspring  # Aktualisiere die Pflanze an der Position
			self.plantDetails(offspring, inner_square_id)  # Zeige Pflanzendetails an

		else:
			# Falls es das Feld noch nicht gibt, was theoretisch nicht passieren sollte, wird es hier behandelt
			print(f'Fehler: Feld {offspring_position} existiert nicht im Grid.')



	def on_GridRightClick(self, event):
		"""
		Behandelt Rechtsklicks auf das Grid und zeigt ein Popup an, wenn der innere Bereich einer Zelle geklickt wird.
		"""
		# Ermittle das angeklickte Canvas-Element
		clicked_item = self.gridCanvas.find_closest(event.x, event.y)
		if clicked_item:
			item_id = clicked_item[0]

			# Finde die (x, y)-Koordinaten der angeklickten Zelle basierend auf der inner-ID
			clicked_position = None
			for position, ids in self.squares.items():
				inner_id = ids.get('inner')  # Hole die ID des inneren Bereichs
				if inner_id == item_id:  # Überprüfe, ob die geklickte ID mit der inner-ID übereinstimmt
					clicked_position = position
					break

			if clicked_position is None:
				print(f'Innerer Bereich der Zelle mit ID {item_id} nicht gefunden.')
				return

			# Prüfe, ob eine Pflanze oder ein Feind ausgewählt ist
			selected_index = self.selectedItem.get()
			if selected_index == -1:
				# Keine Auswahl getroffen
				return

			# Überprüfe, ob an dieser Position eine Pflanze existiert
			plant = self.grid.getPlantAt(clicked_position)
			if plant:
				# Zeige das Popup nur, wenn eine Pflanze existiert
				self.show_popup(clicked_position, event)
			else:
				print(f'Keine Pflanze an Position {clicked_position}.')


	def remove_fieldColor(self):
		"""
		Aktualisiert die Feldfarben basierend auf dem Zustand der Pflanzen und entfernt Tooltips, wenn die Pflanze entfernt wird.
		Setzt auch die Farbe auf Weiß, wenn die Pflanze tot ist und das Feld nicht bereits weiß ist.
		"""
		with self.lock:
			# Durchlaufe alle Positionen und Pflanzen
			for gridID, plant in list(self.plant_at_position.items()):
				# Überprüfe, ob die Pflanze null oder tot ist
				if not plant:
					continue
				self.gridCanvas.after(10)
				# Hole die aktuelle Farbe des Feldes
				current_color = self.gridCanvas.itemcget(gridID, 'fill')
				# Wenn die Pflanze tot ist (currEnergy < minEnergy)
				if plant.currEnergy < plant.minEnergy and current_color != 'white':
					self.set_white(gridID, plant)
					

	def set_white(self, canvas_id, plant):
		"""
		Setzt die Farbe des Feldes auf Weiß und entfernt alle Verbindungen, wenn die Pflanze tot ist.
		"""
		try:
			# Hole das äußere Rechteck
			square_ids = self.squares.get(plant.position)
			if square_ids:
				outer_square_id = square_ids['outer']
				# Setze auch das äußere Rechteck auf Weiß
				self.gridCanvas.itemconfig(outer_square_id, fill='white')
			
			# Setze die Farbe auf Weiß für das innere Rechteck
			self.gridCanvas.itemconfig(canvas_id, fill='white')
			# Entferne alle Verbindungen zu dieser Pflanze
			self.remove_plant_connections(plant)
			self.remove_tooltip(canvas_id)
			self.grid.removePlant(plant)

		except Exception as e:
			print(f'Fehler beim Setzen der Farbe oder Entfernen der Verbindungen für {canvas_id}: {e}')


	def remove_plant_connections(self, plant):
		"""
		Entfernt alle Verbindungen (Linien) von und zu dieser Pflanze.
		"""
		# Entferne alle Verbindungen zu dieser Pflanze
		for (p1, p2), line_id in list(self.grid_lines.items()):
			if p1 == plant or p2 == plant:
				# Lösche die Linie, wenn einer der beiden Pflanzen betroffen ist
				self.gridCanvas.delete(line_id)  # Entferne die Linie vom Canvas
				del self.grid_lines[(p1, p2)]  # Lösche die Verbindung aus dem Dict

		# Lösche auch die Pflanzverbindungen
		for (p1, p2) in list(self.plant_connections.items()):
			if p1 == plant or p2 == plant:
				del self.connect_plants[(p1, p2)]  # Löscht die Verbindung aus dem Dict
				del self.connect_plants[(p2, p1)]  # Löscht auch die Gegenrichtung


	def remove_tooltip(self, square_id):
		"""
		Entfernt den Tooltip für ein bestimmtes Feld.
		"""
		# Entferne alle Binds für den Tooltip
		self.gridCanvas.tag_unbind(square_id, '<Enter>')
		self.gridCanvas.tag_unbind(square_id, '<Leave>')

		# Falls ein Tooltip aktuell angezeigt wird, lösche ihn
		if hasattr(self, 'tooltip_ids'):
			for item_id in self.tooltip_ids:
				self.gridCanvas.delete(item_id)
			del self.tooltip_ids


	def update_enemyMarker(self, old_new_positions):
		"""
		Aktualisiert die Position des Markers auf dem Canvas, wenn der Feind verschoben wird.
		Entfernt den Marker, wenn die Clustergröße 0 erreicht.
		"""
		for cluster, (old_position, new_position) in old_new_positions.items():
			# Berechne die neue Position für den Cluster
			position_data = self.get_cellPosition(new_position)
			if not position_data:
				print(f'Fehler: Ungültige neue Position {new_position}.')
				continue
			x_pos, y_pos = position_data

			# Entferne den Marker des Clusters von der alten Position
			if old_position in self.enemies_at_positions:
				if cluster in self.enemies_at_positions[old_position]:
					if hasattr(cluster, 'circle_id') and cluster.circle_id:
						self.gridCanvas.delete(cluster.circle_id)
					self.enemies_at_positions[old_position].remove(cluster)
					if not self.enemies_at_positions[old_position]:
						del self.enemies_at_positions[old_position]

			# Füge den Marker an der neuen Position hinzu
			fill_color = 'red' if cluster.intoxicated == True else 'navy'  # Setze die Farbe basierend auf dem Vergiftungszustand
			cluster.circle_id = self.create_clusterCircle(x_pos, y_pos, fill_color)
			self.enemies_at_positions.setdefault(new_position, []).append(cluster)


	def remove_dead_cluster(self, old_new_positions):
		"""
		Entfernt Marker von Clustern, deren Größe 0 erreicht hat.
		"""
		for cluster, (old_position, new_position) in old_new_positions.items():
			if cluster.num <= 0:
				print('Cluster ist tot, Marker wird entfernt.')  # Debugging-Ausgabe
				if hasattr(cluster, 'circle_id') and cluster.circle_id:
					self.gridCanvas.delete(cluster.circle_id)  # Entferne den Marker
					print(f'Marker für {cluster.enemy.name} wurde entfernt.')
				# Entferne das Cluster aus der Position
				if old_position in self.enemies_at_positions:
					if cluster in self.enemies_at_positions[old_position]:
						self.enemies_at_positions[old_position].remove(cluster)
						if not self.enemies_at_positions[old_position]:
							del self.enemies_at_positions[old_position]


	def show_substance(self):
		"""
		Aktualisiert die Farben der äußeren Rechtecke basierend auf dem Status von Signalen und Toxinen.
		Die Farben werden nach einer Hierarchie priorisiert:
		1. coral1 (Toxin alarmiert)
		2. Rot (Toxin vorhanden)
		3. Gelb (Signal alarmiert)
		4. Orange (Signal präsent)
		5. Weiß (keine Aktivität)
		"""
		for plant in self.grid.plants:
			square_ids = self.squares.get(plant.position)
			if square_ids:
				square_id = square_ids['outer']

				# Hierarchische Prüfung der Farben
				if any(plant.toxinAlarms.values()):  # Toxin alarmiert
					new_fill_color = 'coral1'
				elif any(plant.isToxically.values()):  # Toxin vorhanden
					new_fill_color = 'red'
				elif any(plant.signalAlarms.values()):  # Signal alarmiert
					new_fill_color = 'yellow'
				elif any(plant.isSignalSignaling.values()):  # Signal präsent, keine Alarmierung
					new_fill_color = 'orange'
				else:
					new_fill_color = 'white'  # Standardfarbe, wenn keine Aktivität vorliegt

				# Letzten bekannten Zustand abfragen
				last_color = self.last_plant_colors.get(plant.position, 'white')

				# Nur aktualisieren, wenn sich die Farbe geändert hat
				if last_color != new_fill_color:
					self.gridCanvas.itemconfig(square_id, fill=new_fill_color)
					self.last_plant_colors[plant.position] = new_fill_color  # Zustand aktualisieren