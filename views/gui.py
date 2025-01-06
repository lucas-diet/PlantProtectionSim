
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import time

from models.grid import Grid
from models.plant import Plant
from models.enemyCluster import Enemy, EnemyCluster
from controllers.simulation import Simulation


class Gui():

	def __init__(self, grid, simulation, diagrams):
		self.grid = grid
		self.simulation = simulation
		self.diagrams = diagrams

		self.initSimulationWindow()
		self.set_breakupsAuto()

		self.PLANT_COLORS = ['#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']
		self.selectedItem = tk.IntVar(value=-1)
		
		self.players = []
		self.enemies_at_positions = {}


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
		
		tk.Button(self.top_frame, text='Breakups', command=self.open_breakupWindow ).grid(row=0, column=10, columnspan=1, pady=1, sticky='ew')
		tk.Button(self.top_frame, text='Play', command=self.run_simulation).grid(row=0, column=11, columnspan=1, pady=1, sticky='ew') ######################################

		tk.Label(self.top_frame, text=' ', width=4).grid(row=0, column=12, padx=1, pady=1, sticky='ew')

		tk.Button(self.top_frame, text='Plot', command=self.open_plotWindow).grid(row=0, column=13, columnspan=1, pady=1, sticky='ew')

		tk.Button(self.top_frame, text='Import').grid(row=0, column=14, columnspan=1, pady=1, sticky='ew')
		tk.Button(self.top_frame, text='Export').grid(row=0, column=15, columnspan=1, pady=1, sticky='ew')


	def createSituation(self):
		self.input_plantsTab()
		self.input_enemiesTab()
		self.input_substancesTab()
		
		self.input_gridSize()
	

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
			row = i * 6
		
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
			
			growEnergy_label = tk.Label(self.plants_setting_frame, text='Growth-Rate:')
			growEnergy_label.grid(row=row+2, column=2, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['growthRate'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['growthRate'].grid(row=row+2, column=3, sticky='ew', padx=2, pady=2)
			
			minEnergy_label = tk.Label(self.plants_setting_frame, text='Min-Energy:')
			minEnergy_label.grid(row=row+3, column=0, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['minEnergy'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['minEnergy'].grid(row=row+3, column=1, sticky='ew', padx=2, pady=2)
			
			repInter_label = tk.Label(self.plants_setting_frame, text='Repro-Interval:')
			repInter_label.grid(row=row+3, column=2, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['reproInterval'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['reproInterval'].grid(row=row+3, column=3, sticky='ew', padx=2, pady=2)
			
			minDist_label = tk.Label(self.plants_setting_frame, text='Min-Distance:')
			minDist_label.grid(row=row+4, column=0, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['minDist'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['minDist'].grid(row=row+4, column=1, sticky='ew', padx=2, pady=2)
			
			maxDist_label = tk.Label(self.plants_setting_frame, text='Max-Distance:')
			maxDist_label.grid(row=row+4, column=2, sticky='w', padx=2, pady=2)
			self.plant_entries[i]['maxDist'] = tk.Entry(self.plants_setting_frame, width=4)
			self.plant_entries[i]['maxDist'].grid(row=row+4, column=3, sticky='ew', padx=2, pady=2)
			
			# Platzhalter für Abstand
			space_label = tk.Label(self.plants_setting_frame, width=4)
			space_label.grid(row=row+5, column=0, padx=2, pady=2, sticky='w')
		
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
			
			speed_label = tk.Label(self.enemies_setting_frame, text='Speed:')
			speed_label.grid(row=row+2, column=2, sticky='w', padx=2, pady=2)
			self.enemy_entries[i]['speed'] = tk.Entry(self.enemies_setting_frame, width=4)
			self.enemy_entries[i]['speed'].grid(row=row+2, column=3, sticky='ew', padx=2, pady=2)
			
			eatingSpeed_label = tk.Label(self.enemies_setting_frame, text='Eat-Speed:')
			eatingSpeed_label.grid(row=row+3, column=0, sticky='w', padx=2, pady=2)
			self.enemy_entries[i]['eatSpeed'] = tk.Entry(self.enemies_setting_frame, width=4)
			self.enemy_entries[i]['eatSpeed'].grid(row=row+3, column=1, sticky='ew', padx=2, pady=2)
			
			eatingVic_label = tk.Label(self.enemies_setting_frame, text='Eat-Victory:')
			eatingVic_label.grid(row=row+3, column=2, sticky='w', padx=2, pady=2)
			self.enemy_entries[i]['eatVictory'] = tk.Entry(self.enemies_setting_frame, width=4)
			self.enemy_entries[i]['eatVictory'].grid(row=row+3, column=3, sticky='ew', padx=2, pady=2)
			
			space_label = tk.Label(self.enemies_setting_frame, width=4)
			space_label.grid(row=row+4, column=0, padx=2, pady=2, sticky='w')
			
		self.enemies_setting_frame.update_idletasks()
		self.enemies_setting_frame.bind('<Configure>', lambda e: self.update_scrollregion(self.enemies_setting_canvas))


	def create_substancesSettings(self, number_of_substances):
		tk.Label(self.substances_setting_frame, text='', width=15).grid(row=0, column=5, padx=1, pady=1, sticky='w')
		
		for i in range(number_of_substances):
			row = i * 10 
			
			# Oberste Zeile: Checkbox und Dropdown
			substance_checkbox = tk.Checkbutton(self.substances_setting_frame, text=f'Substance {i+1}:')
			substance_checkbox.grid(row=row, column=0, sticky='w', padx=2, pady=2)

			substance_options = ['Signal', 'Toxin']  # Dropdown-Optionen
			substance_var = tk.StringVar()
			substance_var.set(substance_options[0])
			substance_menu = tk.OptionMenu(self.substances_setting_frame, substance_var, *substance_options)
			substance_menu.grid(row=row, column=1, padx=2, pady=2, sticky='w')
			substance_menu.config(fg='black', width=5)
			
			toxin_effect_checkbox = tk.Checkbutton(self.substances_setting_frame, text='Deadly Toxin')
			toxin_effect_checkbox.grid(row=row, column=2, padx=2, pady=2, sticky='w')
			toxin_effect_checkbox.config(state='disable')
			
			# Darunter: Spread-Type Label und Dropdown
			spreadType_label = tk.Label(self.substances_setting_frame, text='Spread:')
			spreadType_label.grid(row=row+1, column=0, padx=2, pady=2, sticky='w')

			substance_spreadtype_options = ['Symbiotic', 'Air']  # Dropdown-Optionen
			substance_spreadtype_var = tk.StringVar()
			substance_spreadtype_var.set(substance_spreadtype_options[0])
			substance_spreadtype_menu = tk.OptionMenu(self.substances_setting_frame, substance_spreadtype_var, *substance_spreadtype_options)
			substance_spreadtype_menu.grid(row=row+1, column=1, padx=2, pady=2, sticky='w')
			substance_spreadtype_menu.config(fg='black', width=5)
			
			# Eingabefeld für den Namen der Substanz (über mehrere Zellen)
			name_label = tk.Label(self.substances_setting_frame, text='Name:')
			name_label.grid(row=row+2, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			name_entry = tk.Entry(self.substances_setting_frame)
			name_entry.grid(row=row+2, column=1, columnspan=4, padx=2, pady=2, sticky='ew')
			
			# Eingabefeld für den Produzenten der Substanz (über mehrere Zellen)
			emit_label = tk.Label(self.substances_setting_frame, text='Producer:')
			emit_label.grid(row=row+3, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			emit_entry = tk.Entry(self.substances_setting_frame)
			emit_entry.grid(row=row+3, column=1, columnspan=4, padx=2, pady=2, sticky='ew')
			
			# Eingabefeld für den Empfänger der Substanz (über mehrere Zellen)
			receive_label = tk.Label(self.substances_setting_frame, text='Receiver:')
			receive_label.grid(row=row+4, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			receive_entry = tk.Entry(self.substances_setting_frame)
			receive_entry.grid(row=row+4, column=1, columnspan=4, padx=2, pady=2, sticky='ew')
			receive_checkbox_var = tk.IntVar()
			
			# Eingabefeld für den Trigger der Substanz (über mehrere Zellen)
			trigger_label = tk.Label(self.substances_setting_frame, text='Trigger:')
			trigger_label.grid(row=row+5, column=0, columnspan=1, padx=2, pady=1, sticky='w')
			trigger_entry = tk.Entry(self.substances_setting_frame)
			trigger_entry.grid(row=row+5, column=1, columnspan=4, padx=2, pady=2, sticky='ew')
			
			# Eingabefeld für den Produktionszeit der Substanz
			prodTime_label = tk.Label(self.substances_setting_frame, text='Prod-Time:')
			prodTime_label.grid(row=row+6, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			prodTime_entry = tk.Entry(self.substances_setting_frame, width=4)
			prodTime_entry.grid(row=row+6, column=1, columnspan=1, padx=2, pady=2, sticky='w')
			
			# Eingabefeld für die Sendegeschwindigkeit (Send-Speed)
			sendSpeed_label = tk.Label(self.substances_setting_frame, text='Send-Speed:')
			sendSpeed_label.grid(row=row+6, column=2, columnspan=1, padx=2, pady=2, sticky='w')
			sendSpeed_entry = tk.Entry(self.substances_setting_frame, width=4)
			sendSpeed_entry.grid(row=row+6, column=3, columnspan=1, padx=2, pady=2, sticky='w')
			
			# Eingabefeld für die Energiekosten (Energy-Costs)
			eCosts_label = tk.Label(self.substances_setting_frame, text='Energy-Costs:')
			eCosts_label.grid(row=row+7, column=0, columnspan=1, padx=2, pady=2, sticky='w')
			eCosts_entry = tk.Entry(self.substances_setting_frame, width=4)
			eCosts_entry.grid(row=row+7, column=1, columnspan=1, padx=2, pady=2, sticky='w')
			
			# Eingabefeld für die Nachwirkzeit (AftereffectTime)
			aft_label = tk.Label(self.substances_setting_frame, text='AfterEffectTime:')
			aft_label.grid(row=row+7, column=2, columnspan=1, padx=2, pady=2, sticky='w')
			aft_entry = tk.Entry(self.substances_setting_frame, width=4)
			aft_entry.grid(row=row+7, column=3, columnspan=1, padx=2, pady=2, sticky='w')
			
			space_label = tk.Label(self.substances_setting_frame, width=4)
			space_label.grid(row=row+8, column=0, padx=2, pady=2, sticky='w')

			# Instanzvariablen für die Felder speichern
			setattr(self, f'substance_var_{i}', substance_var)
			setattr(self, f'substance_menu_{i}', substance_menu)
			setattr(self, f'toxin_effect_checkbox_{i}', toxin_effect_checkbox)
			setattr(self, f'substance_spreadtype_menu_{i}', substance_spreadtype_menu)
			setattr(self, f'aft_entry_{i}', aft_entry)
			setattr(self, f'receive_entry_{i}', receive_entry)
			setattr(self, f'sendSpeed_entry_{i}', sendSpeed_entry)

			# Ereignis an Substanzmenü binden, um den ausgewählten Wert zu überprüfen
			substance_var.trace_add('write', lambda *args, i=i: self.change_SubstanceType(i))
				
			
		self.substances_setting_frame.update_idletasks()
		# Scrollregion aktualisieren, wenn das Frame konfiguriert wird
		self.substances_setting_frame.bind('<Configure>',lambda e: self.update_scrollregion(self.substances_setting_canvas))


	def change_SubstanceType(self, index):
		# Zugriff auf Instanzvariablen basierend auf dem Index
		substance_var = getattr(self, f'substance_var_{index}')
		substance_spreadtype_menu = getattr(self, f'substance_spreadtype_menu_{index}')
		toxin_effect_checkbox = getattr(self, f'toxin_effect_checkbox_{index}')
		aft_entry = getattr(self, f'aft_entry_{index}')
		receive_entry = getattr(self, f'receive_entry_{index}')
		sendSpeed_entry = getattr(self, f'sendSpeed_entry_{index}')

		# Disable or enable fields based on the substance type
		if substance_var.get() == 'Toxin':
			substance_spreadtype_menu.config(state='disabled')
			sendSpeed_entry.config(state='disabled')
			toxin_effect_checkbox.config(state='normal')
			receive_entry.config(state='disable')
			aft_entry.config(state='disabled')
		else:
			substance_spreadtype_menu.config(state='normal')
			sendSpeed_entry.config(state='normal')
			toxin_effect_checkbox.config(state='disable')
			receive_entry.config(state='normal')
			aft_entry.config(state='normal')
			

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

		# Tab 1: Pflanzen - Energy
		self.plants_energy_plot_tab = tk.Frame(self.plot_tabs)
		self.plot_tabs.add(self.plants_energy_plot_tab, text='Plants-Energy')
		self.diagrams.dataPlotter(
			root=self.plants_energy_plot_tab,
			data_dict=self.grid.plantData,
			simLength=self.simulation.simLength,
			measure='energy',
			title='Energy by Plant Type Over Time',
			ylabel='Energy'
		)

		# Tab 2: Pflanzen - Count
		self.plants_count_plot_tab = tk.Frame(self.plot_tabs)
		self.plot_tabs.add(self.plants_count_plot_tab, text='Plants-Count')
		self.diagrams.dataPlotter(
			root=self.plants_count_plot_tab,
			data_dict=self.grid.plantData,
			simLength=self.simulation.simLength,
			measure='count',
			title='Number by Plant Types Over Time',
			ylabel='Count'
		)

		# Tab 3: Feinde - Size
		self.enemies_size_plot_tab = tk.Frame(self.plot_tabs)
		self.plot_tabs.add(self.enemies_size_plot_tab, text='Enemies-Size')
		self.diagrams.dataPlotter(
			root=self.enemies_size_plot_tab,
			data_dict=self.grid.EnemyData,
			simLength=self.simulation.simLength,
			measure='size',
			title='Clustersize by Enemy Type Over Time',
			ylabel='Size'
		)

		# Tab 4: Feinde - Count
		self.enemies_count_plot_tab = tk.Frame(self.plot_tabs)
		self.plot_tabs.add(self.enemies_count_plot_tab, text='Enemies-Count')
		self.diagrams.dataPlotter(
			root=self.enemies_count_plot_tab,
			data_dict=self.grid.EnemyData,
			simLength=self.simulation.simLength,
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
			self.maxSteps = int(self.maxStepsBreakup_entry.get()) if self.maxEnemiesBreakup_entry.get() else None
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


	def create_gridFrame(self, width, height):
		self.grid_frame = tk.Frame(self.right_frame, bg='white')
		self.grid_frame.pack_propagate(False)  # Verhindert, dass der Frame seine Größe an Inhalte anpasst
		self.grid_frame.pack(fill='both', expand=True)

		# Canvas für das Grid
		self.gridCanvas = tk.Canvas(self.grid_frame, bg='white', bd=0, relief='solid')
		self.gridCanvas.pack(fill='both', expand=True)

		# Registriere den Event-Handler für Mausklicks
		self.gridCanvas.bind('<Button-1>', self.on_GridClick_player)

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
				x1 = x_offset + i * square_width
				y1 = y_offset + j * square_height
				x2 = x1 + square_width
				y2 = y1 + square_height 
				squareID = self.gridCanvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='white', width=1)
				self.squares[(i,j)] = squareID


	def on_GridClick_player(self, event):
		# Ermittle die angeklickte Zelle
		clicked_item = self.gridCanvas.find_closest(event.x, event.y)
		if clicked_item:
			item_id = clicked_item[0]

			# Finde die (x, y)-Koordinaten der angeklickten Zelle
			clicked_position = None
			for position, id in self.squares.items():
				if id == item_id:
					clicked_position = position
					break

			if clicked_position is None:
				print(f'Zelle mit ID {item_id} nicht gefunden.')
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
		square_id = self.squares.get(position)
		
		if square_id:
			# Hole die Eingabewerte für die Pflanze
			plant_entries = self.plant_entries[selected_index]
			
			# Überprüfe, ob alle Eingabewerte gültig sind (nicht leer und im richtigen Format)
			try:
				init_energy, growth_rate, min_energy, repro_interval, min_dist, max_dist = self.get_plantInputs(plant_entries)
			except ValueError:
				# Falls ein Wert ungültig ist, gebe eine Fehlermeldung aus
				self.error_plants.config(text='Error: All input values ​​must be valid numbers!', fg='red')
				return  # Beende die Funktion ohne die Pflanze hinzuzufügen

			# Überprüfe, ob alle Eingabewerte nicht leer sind (außer repro_interval)
			if not all([init_energy, growth_rate, min_energy, min_dist, max_dist]):
				self.error_plants.config(text='Error: All fields must be filled in!', fg='red')
				return  # Beende die Funktion ohne die Pflanze hinzuzufügen

			# Färbe die angeklickte Zelle
			plant_color = self.PLANT_COLORS[selected_index]
			self.gridCanvas.itemconfig(square_id, fill=plant_color)
			
			# Erzeuge und füge Pflanze hinzu
			plant = self.create_add_plant(selected_index, position, init_energy, growth_rate, min_energy, repro_interval, min_dist, max_dist, plant_color)
			self.plantDetails(plant, square_id)
	

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
				
		min_dist = int(plant_entries['minDist'].get())
		max_dist = int(plant_entries['maxDist'].get())
		if max_dist < min_dist:
			max_dist = min_dist + 1
		else:
			pass

		return init_energy, growth_rate, min_energy, repro_interval, min_dist, max_dist
	

	def create_add_plant(self, selected_index, position, init_energy, growth_rate, min_energy, repro_interval, min_dist, max_dist, plant_color):
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
				reproductionIntervall=repro_interval,
				minDist=min_dist,
				maxDist=max_dist,
				position=position,
				grid=self.grid,
				color=plant_color)

		self.error_plants.config(text='')  # Fehlerbehandlung zurücksetzen
		# Pflanze zur Grid hinzufügen
		if plant not in self.grid.plants:
			self.grid.addPlant(plant)
		else:
			pass
		print(self.grid.plants)
		return plant
	

	def plantDetails(self, plant, square_id):
		"""
		Zeigt die Energie der Pflanze als Tooltip an, wenn die Maus über die Zelle bewegt wird.
		"""
		# Berechne die Energie der Pflanze
		energy_percentage = int((plant.currEnergy / plant.initEnergy) * 100)

		# Funktion zum Anzeigen des Tooltips
		def show_tooltip(event):
			# Berechne die Position der Maus
			x, y = event.x, event.y
			
			# Berechne die Textgröße und die Bounding Box
			tooltip_text = f'Name: {plant.name}\nEnergy: {energy_percentage}%\nPosition: {plant.position}'
			text_id = self.gridCanvas.create_text(
				x + 10, y - 10,  # Text leicht versetzt von der Maus
				text=tooltip_text,
				font=('Arial', 15),
				fill='black',
				anchor='nw'  # Text oben links ausrichten
			)
			bbox = self.gridCanvas.bbox(text_id)  # Bounding Box des Textes

			# Zeichne ein Rechteck als Hintergrund
			if bbox:
				rect_id = self.gridCanvas.create_rectangle(
					bbox[0] - 5, bbox[1] - 2,  # Leichtes Padding um den Text
					bbox[2] + 5, bbox[3] + 2,
					fill='white',  # Hintergrundfarbe
					outline='black',  # Rahmenfarbe
					width=1  # Rahmenbreite
				)
				# Das Rechteck hinter den Text verschieben
				self.gridCanvas.tag_lower(rect_id, text_id)

			# Speichern der IDs für späteres Entfernen
			self.tooltip_ids = (rect_id, text_id)

		# Funktion zum Verstecken des Tooltips
		def hide_tooltip(event):
			if hasattr(self, 'tooltip_ids'):
				for item_id in self.tooltip_ids:
					self.gridCanvas.delete(item_id)
				del self.tooltip_ids

		# Binde die Maus-Events an das Zellen-Item
		self.gridCanvas.tag_bind(square_id, '<Enter>', show_tooltip)  # Tooltip anzeigen, wenn Maus die Zelle betritt
		self.gridCanvas.tag_bind(square_id, '<Leave>', hide_tooltip)  # Tooltip verstecken, wenn Maus die Zelle verlässt


	def enemyClusterPlacer(self, clicked_position, selected_index):
		"""
		Platziert einen Feind-Cluster auf dem Grid an den gegebenen Koordinaten (x, y).
		"""
		square_id = self.squares.get(clicked_position)

		if square_id:
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
			#self.gridCanvas.itemconfig(square_id, fill='red')
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
		enemy = Enemy(name=f'e{selected_index}', symbol=f'E{selected_index}')

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

		# Berechne die Pixelposition aus den Gitterkoordinaten
		x_pos, y_pos = self.get_cellPosition(clicked_position)

		# Feindname und Clustergröße
		enemy_name = cluster.enemy.name  
		circle_id = self.create_clusterCircle(x_pos, y_pos, enemy_name)  # Feindinformationen speichern

		# Speichere die Marker-ID im Cluster
		cluster.circle_id = circle_id

		# Feindinformationen für diese Position speichern  
		if clicked_position not in self.enemies_at_positions:
			self.enemies_at_positions[clicked_position] = []  # Initialisiere Liste für diese Position, falls sie noch nicht existiert

		# Füge die Feindinformationen zur Liste hinzu
		self.enemies_at_positions[clicked_position].append(cluster)

		# Füge Tooltip hinzu
		self.addTooltip(circle_id, clicked_position)

		print(f'Feind {enemy_name} mit Clustergröße {cluster.num} platziert auf: {clicked_position}')



	def get_cellPosition(self, position):
		"""
		Berechnet die Position der Zelle basierend auf den Koordinaten und berücksichtigt Scroll-Offsets.
		"""
		square_id = self.squares.get(position)  # Erhalte die Zellen-ID von den Koordinaten
		if square_id is None:
			print(f'Fehler: Keine Zelle mit den Koordinaten {position} gefunden.')
			return None  # Zelle nicht gefunden

		bbox = self.gridCanvas.bbox(square_id)
		if bbox is None:
			print(f'Fehler: Keine Bounding Box für die Zelle mit item_id {square_id} gefunden.')
			return None  # Bounding Box nicht gefunden

		cell_width = bbox[2] - bbox[0]
		cell_height = bbox[3] - bbox[1]
		x_pos = bbox[0] + cell_width / 2
		y_pos = bbox[1] + cell_height / 2

		if not hasattr(self, 'enemy_positions'):
			self.enemy_positions = {}

		if position not in self.enemy_positions:
			self.enemy_positions[position] = 0

		current_enemy_count = self.enemy_positions[position]
		y_pos += current_enemy_count * 15  # Verschiebe die Y-Position für mehrere Feinde in derselben Zelle

		return x_pos, y_pos
	
	
	def create_clusterCircle(self, x_pos, y_pos, enemy_name): 
		""" Zeichnet einen kleinen Kreis, um den Feind auf dem Canvas darzustellen. """

		circle_radius = 2.5  # Kleinere Kreisgröße für den Feind 
		
		# Berechne die Koordinaten für den Kreis (Bounding Box: (left, top, right, bottom)) 
		left = x_pos - circle_radius 
		top = y_pos - circle_radius 
		right = x_pos + circle_radius 
		bottom = y_pos + circle_radius # Zeichne den Kreis 
		circle_id = self.gridCanvas.create_oval(left, top, right, bottom, fill='red', outline='black') 
		return circle_id
	

	def addTooltip(self, circle_id, position):
		"""
		Fügt Tooltip-Logik für einen Canvas-Text hinzu.
		"""
		# Funktion zum Anzeigen des Tooltips
		def show_tooltip(event):
			x, y = event.x, event.y
			tooltip_text = []

			# Sammle Informationen zu allen Feinden an dieser Position
			enemies_at_pos = self.enemies_at_positions.get(position, [])
			for ec in enemies_at_pos:
				tooltip_text.append(f'{ec.enemy.name}: Size {int(ec.num)}')

			# Verarbeite die Tooltip-Texte zu einer mehrzeiligen Darstellung
			tooltip_full_text = '\n'.join(tooltip_text)

			# Erstelle den Tooltip-Text
			tooltip_text_id = self.gridCanvas.create_text(
				x + 10, y - 10,  # Text leicht versetzt von der Maus
				text=tooltip_full_text,
				font=('Arial', 15),
				fill='black',
				anchor='nw'  # Text oben links ausrichten
			)

			# Berechne die Bounding Box für den Tooltip-Text
			bbox = self.gridCanvas.bbox(tooltip_text_id)

			# Erstelle ein Rechteck als Hintergrund
			if bbox:
				rect_id = self.gridCanvas.create_rectangle(
					bbox[0] - 5, bbox[1] - 2,  # Leichtes Padding um den Text
					bbox[2] + 5, bbox[3] + 2,
					fill='white',  # Hintergrundfarbe
					outline='black',  # Rahmenfarbe
					width=1  # Rahmenbreite
				)
				# Setze das Rechteck hinter den Text
				self.gridCanvas.tag_lower(rect_id, tooltip_text_id)

			# Speichere die IDs für späteres Entfernen
			self.tooltip_ids = (rect_id, tooltip_text_id)

		# Funktion zum Verstecken des Tooltips
		def hide_tooltip(event):
			if hasattr(self, 'tooltip_ids'):
				for item_id in self.tooltip_ids:
					self.gridCanvas.delete(item_id)
				del self.tooltip_ids

		# Binde die Maus-Events an das Text-Item
		self.gridCanvas.tag_bind(circle_id, '<Enter>', show_tooltip)  # Tooltip anzeigen, wenn Maus das Text-Item betritt
		self.gridCanvas.tag_bind(circle_id, '<Leave>', hide_tooltip)  # Tooltip verstecken, wenn Maus das Text-Item verlässt


	def run_simulation(self):
		sim = Simulation(self.grid)
		count = 1
		while True:
			if count - 1 == self.maxSteps:
				break
			if sim.noSpecificPlantBreak(self.plant_death):
				break
			if sim.noSpeceficEnemyBreak(self.enemy_death):
				break
			if sim.noEnemiesBreak():
				break
			if sim.noPlantsBreak():
				break
			if sim.upperGridEnergyBreak(self.max_plant_energy):
				break
			if sim.upperEnemyNumBreak(self.max_enemies_num):
				break

			# Feinde sammeln und bewegen (alle gleichzeitig)
			old_positions = {ec: ec.position for ec in self.grid.enemies}
			self.grid.collectAndManageEnemies()  # Alle Cluster bewegen
			new_positions = {ec: ec.position for ec in self.grid.enemies}
			for ec in self.grid.enemies:
				old_position = old_positions[ec]
				new_position = new_positions[ec]
				self.update_enemyMarker(old_position, new_position, ec.enemy.symbol, ec)
			count += 1
			self.gridCanvas.after(500)


	def update_enemyMarker(self, old_position, new_position, selected_index, cluster):
		"""
		Aktualisiert die Position des Markers auf dem Canvas, wenn der Feind verschoben wird.
		"""
		# Berechne die neue Position für den Cluster
		position_data = self.get_cellPosition(new_position)
		if not position_data:
			print(f'Fehler: Ungültige neue Position {new_position}.')
			return
		x_pos, y_pos = position_data

		# Entferne den Marker des Clusters von der alten Position
		if old_position in self.enemies_at_positions:
			# Prüfe, ob der Cluster an der alten Position existiert
			if cluster in self.enemies_at_positions[old_position]:
				# Lösche den Marker, falls vorhanden
				if hasattr(cluster, 'circle_id') and cluster.circle_id:
					self.gridCanvas.delete(cluster.circle_id)
				# Entferne den Cluster aus der alten Position
				self.enemies_at_positions[old_position].remove(cluster)
				# Wenn die alte Position leer ist, entferne sie aus dem Dictionary
				if not self.enemies_at_positions[old_position]:
					del self.enemies_at_positions[old_position]

		# Aktualisiere die Position des Clusters
		cluster.position = new_position

		# Erstelle einen neuen Marker für die neue Position
		circle_id = self.create_clusterCircle(x_pos, y_pos, cluster.enemy.name)
		cluster.circle_id = circle_id  # Speichere die Marker-ID im Cluster

		# Füge den Cluster zur neuen Position hinzu
		if new_position not in self.enemies_at_positions:
			self.enemies_at_positions[new_position] = []
		self.enemies_at_positions[new_position].append(cluster)

		# Tooltip aktualisieren
		self.addTooltip(circle_id, new_position)
		self.gridCanvas.update_idletasks()
		print(f'Feind {cluster.enemy.name} von {old_position} nach {new_position} verschoben.')
		






'''

# Wenn es einen alten Marker gibt, lösche ihn
		if cluster:
			if old_position in self.enemies_at_positions:
				for enemy in self.enemies_at_positions[old_position]:
					if enemy['name'] == cluster.enemy.name and 'circle_id' in enemy:
						print(f'Entferne alten Marker: {enemy['circle_id']}')
						self.gridCanvas.delete(enemy['circle_id'])  # Lösche den alten Marker
						# Entferne den Eintrag aus der alten Position
						self.enemies_at_positions[old_position] = [
							enemy for enemy in self.enemies_at_positions[old_position]
							if enemy['name'] != cluster.enemy.name 
						]
						if not self.enemies_at_positions[old_position]:
							del self.enemies_at_positions[old_position]

				# Erstelle den neuen Marker
				circle_id = self.create_clusterCircle(x_pos, y_pos, cluster.enemy.name)
				self.addTooltip(circle_id, new_position)

				# Füge die neue Position zur Liste hinzu
				if new_position not in self.enemies_at_positions:
					self.enemies_at_positions[new_position] = []
				self.enemies_at_positions[new_position].append({
					'name': cluster.enemy.name,
					'circle_id': circle_id,  # Speichere die neue Marker-ID
					'clusterSize': len(self.enemies_at_positions.get(new_position, [])) + 1
				})

				# Stelle sicher, dass das Canvas aktualisiert wird
				self.gridCanvas.update_idletasks()
				print(f'{old_position} -> {new_position}')
'''
