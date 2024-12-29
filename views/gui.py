
import tkinter as tk
from tkinter import ttk


class Gui():
	def __init__(self, grid, simulation, diagrams):
		self.grid = grid
		self.simulation = simulation
		self.diagrams = diagrams

		self.root = tk.Tk()
		self.root.title('Simulator')
		self.PLANT_COLORS = ['#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']
		
		self.windowSize()
		self.createAreas()
		
		self.selectedItem = tk.IntVar(value=-1)
		self.players = []
		
	
	def mainloop(self):
		self.root.mainloop()
	

	def windowSize(self):
		# Berechnen der Fenstergröße
		window_width = self.root.winfo_screenwidth() - 200
		window_height = self.root.winfo_screenheight() - 200
		
		# Berechnung der Position, um das Fenster zu zentrieren
		center_x = int(self.root.winfo_screenwidth() / 2 - window_width / 2)
		center_y = int(self.root.winfo_screenheight() / 2 - window_height / 2)
		
		# Setzen der Fenstergröße und Position
		self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
		
		
	def createAreas(self):
		# Bereich oben
		self.top_frame = tk.Frame(self.root)
		self.top_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
		self.topAreaWidgets()
		
		# Bereich links (Sidebar)
		self.left_frame = tk.Frame(self.root, bg='lightgreen')
		self.left_frame.grid(row=1, column=0, sticky='nsew')
		
		# Tabs in der Sidebar
		self.createSidebarTabs()
		
		# Bereich rechts
		self.right_frame = tk.Frame(self.root, padx=10, pady=10, bg='darkgray')
		self.right_frame.grid(row=1, column=1, sticky='nsew')
		
		
		# Spalten und Zeilen skalierbar machen
		self.root.grid_rowconfigure(0, weight=0)  # Oben
		self.root.grid_rowconfigure(1, weight=6)  # Mitte
		self.root.grid_columnconfigure(0, weight=2)  # Links
		self.root.grid_columnconfigure(1, weight=9, uniform='equal')  # Rechts


	def createSidebarTabs(self):
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
		apply_button = tk.Button(self.top_frame, text='Apply', command=self.createSituation)
		apply_button.grid(row=0, column=8, columnspan=1, pady=1)
		
		tk.Label(self.top_frame, text=' ', width=4).grid(row=0, column=9, padx=1, pady=1, sticky='ew')
		
		tk.Button(self.top_frame, text='Simulate').grid(row=0, column=10, columnspan=1, pady=1, sticky='ew')
		tk.Button(self.top_frame, text='Import').grid(row=0, column=11, columnspan=1, pady=1, sticky='ew')
		tk.Button(self.top_frame, text='Export').grid(row=0, column=12, columnspan=1, pady=1, sticky='ew')
		tk.Button(self.top_frame, text='Plot', command=self.openPlotWindow).grid(row=0, column=13, columnspan=1, pady=1, sticky='ew')
		
	
	def createSituation(self):
		self.createPlants_tab()
		self.createEnemies_tab()
		self.createSubstances_tab()
		
		self.createBattlefield()
		
	
	def createPlants_tab(self):
		try:
			# Eingabe in eine Zahl umwandeln
			number_of_plants = int(self.plants_entry.get())
		except ValueError:
			# Fehlerbehandlung, falls die Eingabe keine gültige Zahl ist
			return
		
		# Überprüfen, ob die Zahl zwischen 0 und 15 liegt
		if number_of_plants < 1 or number_of_plants > 16:
			self.clear_plants_frame()  # Lösche bestehende Elemente
			print('The number of plants must be between 1 and 16!')
			return
		
		# Bereinigen bestehender Widgets, falls die Frame bereits existiert
		if hasattr(self, 'plants_setting_frame'):
			self.clear_plants_frame()
		else:
			# Erstellen von Canvas, Frame und Scrollbar
			self.create_canvas_and_frame_plants()
		# Substanzen-Einstellungen erstellen
		self.create_plants_settings(number_of_plants)
		
	
	def clear_plants_frame(self):
		"""Bereinigt alle Widgets im Frame der Substanzen"""
		if hasattr(self, 'plants_setting_frame'):
			for widget in self.plants_setting_frame.winfo_children():
				widget.destroy()
				
	
	def create_canvas_and_frame_plants(self):
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
				
	
	def create_plants_settings(self, number_of_plants):
		"""Erstellt die Einstellungen für Pflanzen."""
		
		# Label für Abstand
		tk.Label(self.plants_setting_frame, text='', width=25).grid(row=0, column=4, padx=1, pady=1, sticky='w')
		
		# Gemeinsame Variable für alle Checkbuttons
		if not hasattr(self, 'selectedPlayer'):
			self.selectedPlayer = tk.IntVar(value=-1)  # -1 bedeutet: Kein Button ausgewählt
			
		for i in range(number_of_plants):
			row = i * 5
					
			# Checkbutton für Pflanze
			plant_checkbox = tk.Checkbutton(
				self.plants_setting_frame,
				variable=self.selectedItem,  # Gemeinsame Variable
				onvalue=i,  # Wert, wenn dieser Checkbutton ausgewählt wird
				offvalue=-1,  # Wert, wenn kein Checkbutton ausgewählt ist
				text=f'Plant {i+1}:'
			)
			plant_checkbox.grid(row=row, column=0, sticky='w', padx=2, pady=2)
			
			# Farbe der Pflanze
			plant_color_label = tk.Label(self.plants_setting_frame, width=2, bg=self.PLANT_COLORS[i])
			plant_color_label.grid(row=row, column=1, sticky='ew', padx=2, pady=2)
			
			# Energie-Label und Eingabefelder
			initEnergy_label = tk.Label(self.plants_setting_frame, text='Init-Energy:')
			initEnergy_label.grid(row=row+1, column=0, sticky='w', padx=2, pady=2)
			initEnergy_entry = tk.Entry(self.plants_setting_frame, width=4)
			initEnergy_entry.grid(row=row+1, column=1, sticky='ew', padx=2, pady=2)
			
			growEnergy_label = tk.Label(self.plants_setting_frame, text='Growth-Rate:')
			growEnergy_label.grid(row=row+1, column=2, sticky='w', padx=2, pady=2)
			growEnergy_entry = tk.Entry(self.plants_setting_frame, width=4)
			growEnergy_entry.grid(row=row+1, column=3, sticky='ew', padx=2, pady=2)
			
			minEnergy_label = tk.Label(self.plants_setting_frame, text='Min-Energy:')
			minEnergy_label.grid(row=row+2, column=0, sticky='w', padx=2, pady=2)
			minEnergy_entry = tk.Entry(self.plants_setting_frame, width=4)
			minEnergy_entry.grid(row=row+2, column=1, sticky='ew', padx=2, pady=2)
			
			repInter_label = tk.Label(self.plants_setting_frame, text='Repro-Interval:')
			repInter_label.grid(row=row+2, column=2, sticky='w', padx=2, pady=2)
			repInter_entry = tk.Entry(self.plants_setting_frame, width=4)
			repInter_entry.grid(row=row+2, column=3, sticky='ew', padx=2, pady=2)
			
			minDist_label = tk.Label(self.plants_setting_frame, text='Min-Distance:')
			minDist_label.grid(row=row+3, column=0, sticky='w', padx=2, pady=2)
			minDist_entry = tk.Entry(self.plants_setting_frame, width=4)
			minDist_entry.grid(row=row+3, column=1, sticky='ew', padx=2, pady=2)
			
			maxDist_label = tk.Label(self.plants_setting_frame, text='Max-Distance:')
			maxDist_label.grid(row=row+3, column=2, sticky='w', padx=2, pady=2)
			maxDist_entry = tk.Entry(self.plants_setting_frame, width=4)
			maxDist_entry.grid(row=row+3, column=3, sticky='ew', padx=2, pady=2)
			
			# Platzhalter für Abstand
			space_label = tk.Label(self.plants_setting_frame, width=4)
			space_label.grid(row=row+4, column=0, padx=2, pady=2, sticky='w')
			
		# Scrollregion aktualisieren
		self.plants_setting_frame.update_idletasks()
		self.plants_setting_frame.bind('<Configure>', lambda e: self.update_scrollregion(self.plants_setting_canvas))
		
		
	def createEnemies_tab(self):
		try:
			# Eingabe in eine Zahl umwandeln
			number_of_enemies = int(self.enemies_entry.get())
		except ValueError:
			# Fehlerbehandlung, falls die Eingabe keine gültige Zahl ist
			return
		
		# Überprüfen, ob die Zahl zwischen 0 und 15 liegt
		if number_of_enemies < 0 or number_of_enemies > 15:
			self.clear_enemies_frame()  # Lösche bestehende Elemente
			print('The number of enemies must be between 1 and 16!')
			return
		
		# Bereinigen bestehender Widgets, falls die Frame bereits existiert
		if hasattr(self, 'enemies_setting_frame'):
			self.clear_enemies_frame()
		else:
			# Erstellen von Canvas, Frame und Scrollbar
			self.create_canvas_and_frame_enemies()
		# Substanzen-Einstellungen erstellen
		self.create_enemies_settings(number_of_enemies)
		
		
	def clear_enemies_frame(self):
		"""Bereinigt alle Widgets im Frame der Substanzen"""
		if hasattr(self, 'enemies_setting_frame'):
			for widget in self.enemies_setting_frame.winfo_children():
				widget.destroy()
				
				
	def create_canvas_and_frame_enemies(self):
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
		
	
	def create_enemies_settings(self, number_of_enemies):
		tk.Label(self.enemies_setting_frame, text='', width=25).grid(row=0, column=4, padx=1, pady=1, sticky='w')
		offset = 16 # Offset, um die Feinde von den Pflanzen in der Variablen zu unterscheiden
		for i in range(number_of_enemies):
			row = i * 9
						
			# Checkbutton für Feind
			enemy_checkbox = tk.Checkbutton(
				self.enemies_setting_frame,
				variable=self.selectedItem,  # Gemeinsame Variable
				onvalue=offset + i,  # Ein eindeutiger Wert für Feinde (Pflanzen sind 0-n, Feinde sind 100+)
				offvalue=-1,  # Wert, wenn kein Checkbutton ausgewählt ist
				text=f'Enemy-Cluster {i+1}:'
			)
			#enemy_checkbox = tk.Checkbutton(self.enemies_setting_frame, text=f'Enemy {i+1}:')
			enemy_checkbox.grid(row=row, column=0, sticky='w', padx=2, pady=2)
			
			clusterNum_label = tk.Label(self.enemies_setting_frame, text='Cluster-Size:')
			clusterNum_label.grid(row=row+1, column=0, sticky='w', padx=2, pady=2)
			clusterNum_entry = tk.Entry(self.enemies_setting_frame, width=4)
			clusterNum_entry.grid(row=row+1, column=1, sticky='ew', padx=2, pady=2)
			
			speed_label = tk.Label(self.enemies_setting_frame, text='Speed:')
			speed_label.grid(row=row+1, column=2, sticky='w', padx=2, pady=2)
			speed_entry = tk.Entry(self.enemies_setting_frame, width=4)
			speed_entry.grid(row=row+1, column=3, sticky='ew', padx=2, pady=2)
			
			eatingSpeed_label = tk.Label(self.enemies_setting_frame, text='Eat-Speed:')
			eatingSpeed_label.grid(row=row+2, column=0, sticky='w', padx=2, pady=2)
			eatingSpeed_entry = tk.Entry(self.enemies_setting_frame, width=4)
			eatingSpeed_entry.grid(row=row+2, column=1, sticky='ew', padx=2, pady=2)
			
			eatingVic_label = tk.Label(self.enemies_setting_frame, text='Eat-Victory:')
			eatingVic_label.grid(row=row+2, column=2, sticky='w', padx=2, pady=2)
			eatingVic_entry = tk.Entry(self.enemies_setting_frame, width=4)
			eatingVic_entry.grid(row=row+2, column=3, sticky='ew', padx=2, pady=2)
			
			space_label = tk.Label(self.enemies_setting_frame, width=4)
			space_label.grid(row=row+3, column=0, padx=2, pady=2, sticky='w')
			

		self.enemies_setting_frame.update_idletasks()
		self.enemies_setting_frame.bind('<Configure>', lambda e: self.update_scrollregion(self.enemies_setting_canvas))
		
	
	def createSubstances_tab(self):
		try:
			# Eingabe in eine Zahl umwandeln
			number_of_substances = int(self.substances_entry.get())
		except ValueError:
			# Fehlerbehandlung, falls die Eingabe keine gültige Zahl ist
			return
		
		# Überprüfen, ob die Zahl zwischen 0 und 15 liegt
		if number_of_substances < 0 or number_of_substances > 15:
			self.clear_substances_frame()  # Lösche bestehende Elemente
			print('The number of substances must be between 0 and 15!')
			return
		
		# Bereinigen bestehender Widgets, falls die Frame bereits existiert
		if hasattr(self, 'substances_setting_frame'):
			self.clear_substances_frame()
		else:
			# Erstellen von Canvas, Frame und Scrollbar
			self.create_canvas_and_frame_substances()
			
		# Substanzen-Einstellungen erstellen
		self.create_substances_settings(number_of_substances)
				
		
	def clear_substances_frame(self):
		"""Bereinigt alle Widgets im Frame der Substanzen"""
		if hasattr(self, 'substances_setting_frame'):
			for widget in self.substances_setting_frame.winfo_children():
				widget.destroy()
		
	
	def create_canvas_and_frame_substances(self):
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
	
	
	def create_substances_settings(self, number_of_substances):
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
			
			# Ereignis an Substanzmenü binden, um den ausgewählten Wert zu überprüfen
			substance_var.trace_add('write', lambda *args, substance_var=substance_var, receive_entry=receive_entry, aft_entry=aft_entry, substance_spreadtype_menu=substance_spreadtype_menu, toxin_effect_checkbox=toxin_effect_checkbox, sendSpeed_entry=sendSpeed_entry: self.substanceType_change(substance_var, receive_entry, aft_entry, substance_spreadtype_menu, toxin_effect_checkbox, sendSpeed_entry))
			
		self.substances_setting_frame.update_idletasks()
		# Scrollregion aktualisieren, wenn das Frame konfiguriert wird
		self.substances_setting_frame.bind('<Configure>',lambda e: self.update_scrollregion(self.substances_setting_canvas))
	
	
	def substanceType_change(self, substance_var, receive_entry, aft_entry, substance_spreadtype_menu, toxin_effect_checkbox, sendSpeed_entry):
		# Disable or enable fields based on the substance type
		if substance_var.get() == 'Toxin':
			receive_entry.config(state='disabled')
			aft_entry.config(state='disabled')
			substance_spreadtype_menu.config(state='disabled')
			sendSpeed_entry.config(state='disable')
			toxin_effect_checkbox.config(state='normal')
		else:
			receive_entry.config(state='normal')
			aft_entry.config(state='normal')
			substance_spreadtype_menu.config(state='normal')
			sendSpeed_entry.config(state='normal')
			toxin_effect_checkbox.config(state='disable')
	
	
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
	

	def createBattlefield(self):
		try:
			# Eingabe in eine Zahl umwandeln
			gridSize = int(self.grid_size_entry.get())
		except ValueError:
			# Fehlerbehandlung, falls die Eingabe keine gültige Zahl ist
			print('Invalid input: Please enter a number.')
			return
		
		# Überprüfen, ob die Zahl zwischen 1 und 80 liegt
		if gridSize < 1 or gridSize > 80:
			print('The number of fields must be between 1 and 80!')
			return
		
		# Bereinigen bestehender Widgets und Frames
		self.clear_grid_frame()
		
		# Neues Canvas und Grid erstellen
		self.create_canvas_and_frame_grid()
			
	
	def clear_grid_frame(self):
		if hasattr(self, 'grid_frame'):
			# Zerstöre alle Kinder-Widgets im Frame
			for widget in self.grid_frame.winfo_children():
				widget.destroy()
			# Lösche den Frame selbst
			self.grid_frame.destroy()
			del self.grid_frame  # Entferne die Referenz auf das Attribut
		
	
	def create_canvas_and_frame_grid(self):
		self.grid_frame = tk.Frame(self.right_frame, bg='white')
		self.grid_frame.pack_propagate(False)  # Verhindert, dass der Frame seine Größe an Inhalte anpasst
		self.grid_frame.pack(fill='both', expand=True)  # Kein expand, um Vergrößerung zu vermeiden
		
		# Canvas für das Grid
		self.gridCanvas = tk.Canvas(self.grid_frame, bg='white', bd=0, relief='solid')
		self.gridCanvas.pack(fill='both', expand=True)
		
		
		#self.root.resizable(False, False)  # Deaktiviert Resize sowohl horizontal als auch vertikal
		
		# Registriere den Event-Handler für Mausklicks
		self.gridCanvas.bind('<Button-1>', self.onGridClick_player)
		#self.gridCanvas.bind("<Button-2>", self.onGridClick_enemies)
		
		# Hole die Grid-Größe aus dem Eingabefeld
		try:
			width = int(self.grid_size_entry.get())
			height = int(self.grid_size_entry.get())
		except ValueError:
			# Fallback bei ungültiger Eingabe
			width, height = 10, 10
			
		# Bereinige die Canvas vor dem Zeichnen
		self.gridCanvas.delete('all')
		
		# Aktualisiere die Canvas-Größe
		self.gridCanvas.update()
		canvas_width = self.gridCanvas.winfo_width()
		canvas_height = self.gridCanvas.winfo_height()
		
		self.calculateSquareSize(width, height, canvas_width, canvas_height)
		
	
	def calculateSquareSize(self, width, height, canvas_width, canvas_height):
		# Berechne die maximale Quadratgröße, aber behalte die Höhe unverändert
		if width > 0 and height > 0:
			square_height = canvas_height / height  # Höhe bleibt unverändert
			square_width = canvas_width / width    # Breite passt sich der Canvas-Breite an
			
			# Verwende die Höhe für die Quadratgröße, damit die Quadrate nicht zu hoch werden
			square_size = square_height
			
			# Berechne die tatsächliche Breite und Höhe des Grids
			grid_width = square_width * width
			grid_height = square_size * height
			
			# Zentriere das Grid, indem du Offsets berechnest
			x_offset = (canvas_width - grid_width) / 2
			y_offset = (canvas_height - grid_height) / 2
			
			self.drawGrid(width, height, x_offset, y_offset, square_width, square_size)
	
	def drawGrid(self, width, height, x_offset, y_offset, square_width, square_size):
		# Zeichne die Quadrate
		self.squares = {}
		for i in range(width):
			for j in range(height):
				x1 = x_offset + i * square_width
				y1 = y_offset + j * square_size
				x2 = x1 + square_width
				y2 = y1 + square_size
				squareID = self.gridCanvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='white', width=1)
				self.squares[squareID] = (x1, y1, x2, y2)
				
				
	def onGridClick_player(self, event):
		# Ermittle die angeklickte Zelle
		clicked_item = self.gridCanvas.find_closest(event.x, event.y)
		if clicked_item:
			item_id = clicked_item[0]
			
			# Prüfe, ob eine Pflanze oder ein Feind ausgewählt ist
			selected_index = self.selectedItem.get()
			
			if selected_index == -1:
				# Keine Auswahl getroffen
				return
			
			# Überprüfen, ob eine Pflanze oder ein Feind ausgewählt wurde
			if selected_index < 16:  # Pflanzen haben Werte von 0 bis 15
				self.place_plant_on_grid(item_id, selected_index)
			else:  # Feinde haben Werte ab 16
				self.place_enemy_on_grid(item_id, selected_index)
	
	
	def place_plant_on_grid(self, item_id, selected_index):
		"""
		Platziert eine Pflanze auf dem Grid.
		"""
		# Entferne eventuell bereits vorhandene Pflanze (wenn die Zelle bereits eine Pflanze enthält)
		if self.gridCanvas.itemcget(item_id, 'fill'):  # Prüfen, ob die Zelle bereits eine Farbe hat
			self.gridCanvas.itemconfig(item_id, fill='')  # Entferne Farbe
		
		# Hole den Grünton der ausgewählten Pflanze
		plant_color = self.PLANT_COLORS[selected_index]
		
		# Färbe die angeklickte Zelle
		self.gridCanvas.itemconfig(item_id, fill=plant_color)
		
		print(f'Pflanze platziert auf: {item_id}')
		
	
	def place_enemy_on_grid(self, item_id, selected_index):
		"""
		Platziert einen Feind auf dem Grid.
		"""
		# Berechne den Feindindex für den Feindnamen
		enemy_name = f'E{selected_index - 15}'  # Feindname anhand des Index
		
		# Zellenposition ermitteln
		bbox = self.gridCanvas.bbox(item_id)
		cell_width = bbox[2] - bbox[0]  # Berechne die Breite der Zelle
		cell_height = bbox[3] - bbox[1]  # Berechne die Höhe der Zelle
		
		# Berechne den Mittelpunkt der Zelle
		x_pos = bbox[0] + cell_width / 2  # X-Mittelpunkt
		y_pos = bbox[1] + cell_height / 2  # Y-Mittelpunkt
		
		# Wenn bereits Feinde auf dem Feld sind, müssen wir die Y-Position für den neuen Feind erhöhen
		if not hasattr(self, 'enemy_positions'):
			self.enemy_positions = {}  # Speichert die Feindpositionen pro Zelle
		if item_id not in self.enemy_positions:
			self.enemy_positions[item_id] = 0  # Zähler für Feinde in dieser Zelle
			
		# Feindnummer basierend auf der Anzahl der Feinde, die bereits auf dieser Zelle sind
		current_enemy_count = self.enemy_positions[item_id]
		y_pos += current_enemy_count * 15  # Verschiebe die Y-Position für jedes zusätzliche Feind-Element
		
		# Erstelle den Text für den Feind
		self.gridCanvas.create_text(
			x_pos, 
			y_pos,
			text=enemy_name,
			font=('Arial', 8),  # Schriftart und -größe
			fill='red'
		)
		
		# Erhöhe den Zähler für Feinde in dieser Zelle
		self.enemy_positions[item_id] += 1
		print(f'Feind platziert auf: {item_id}')

	
	def openPlotWindow(self):
		"""
		Öffnet ein neues Fenster, um die Plots anzuzeigen.
		
		Args:
			data_dict (dict): Ein Dictionary mit den Daten.
			simLength (int): Die Anzahl der Zeitschritte.
			measure1 (str): Die erste Messgröße ('energy' oder 'size').
			measure2 (str): Die zweite Messgröße ('count').
			title1 (str): Titel des ersten Subplots.
			title2 (str): Titel des zweiten Subplots.
		"""
		# Neues Tkinter-Fenster erstellen
		self.plotWindow = tk.Tk()
		self.plotWindow.title('Plot Window')

		self.plot_tabs = ttk.Notebook(self.plotWindow)
		
		# Tab 1: Pflanzen
		self.plants_plot_tab = tk.Frame(self.plotWindow)
		self.plot_tabs.add(self.plants_plot_tab, text='Plants')
		
		# Tab 2: Feinde
		self.enemies_plot_tab = tk.Frame(self.plotWindow)
		self.plot_tabs.add(self.enemies_plot_tab, text='Enemies')
		self.plot_tabs.pack(fill='both', expand=True)
		
		# Plot in das neue Fenster einbinden
		self.diagrams.dataPlotter(
			root=self.plants_plot_tab,
			data_dict=self.grid.plantData,
			simLength=self.simulation.simLength,
			measure1='energy',
			measure2='count',
			title1='Energy by Plant Type Over Time',
			title2='Number by Plant Types Over Time'
		)
		self.diagrams.dataPlotter(
			root=self.enemies_plot_tab,
			data_dict=self.grid.EnemyData,
			simLength=self.simulation.simLength,
			measure1='size',
			measure2='count',
			title1='Clustersize by Enemy Type Over Time',
			title2='Number by Enemy Types Over Time'
		)

