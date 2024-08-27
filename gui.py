
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from tooltip import Tooltip

class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Initital Configuration')
        
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()-200

        window_width = 300
        window_height = 300

        center_x = int(self.screen_width / 2 - window_width / 2)
        center_y = int(self.screen_height / 2 - window_height / 2)
        
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.createInitWindow()
        
        self.colorList_p = ['#00FF00', '#32CD32', '#228B22', '#006400', '#7CFC00', '#00FF7F', '#2E8B57', '#3CB371', '#20B2AA', '#48D1CC', '#00FA9A', '#66CDAA', '#8FBC8F', '#98FB98', '#9ACD32', '#6B8E23']
        self.colorList_h = ['#FF0000', '#FF6347', '#FF4500', '#FF1493', '#DC143C', '#C8102E', '#B22222', '#8B0000', '#E9967A', '#F08080', '#F4A460', '#D70040', '#C71585', '#FF6F61', '#FF8C00']
        self.colors = []

        # Hold the ID of selected squares
        self.selected_squares = []
       
    def createInitWindow(self):
        numPlant_lab = tk.Label(text='number plants')
        numherbi_lab = tk.Label(text='number herbivores')
        numPlant_lab.place(x=10, y=10)
        numherbi_lab.place(x=10, y=50)

        # Validierungsfunktionen Teams
        valiPlants_in = (self.window.register(self.inputValidation), '%P', '%W', 1, 16)
        valiHerbi_in = (self.window.register(self.inputValidation), '%P', '%W', 0, 15)

        self.numPlant_in = tk.Entry(width=10, validate='key', validatecommand=valiPlants_in)
        self.numHerbi_in = tk.Entry( width=10, validate='key', validatecommand=valiHerbi_in)
        self.numPlant_in.config(bg='white', fg='black')
        self.numHerbi_in.config(bg='white', fg='black')
        self.numPlant_in.place(x=130, y=10)
        self.numHerbi_in.place(x=130, y=50)

        girdSize_lab = tk.Label(text='grid size')
        girdSize_lab.place(x=10, y=100)

        # Validierungsfunktionen Grid
        valiGrid_in = (self.window.register(self.inputValidation), '%P', '%W', 1, 80)

        self.girdSize_in = tk.Entry(width=10, validate='key', validatecommand=valiGrid_in)
        self.girdSize_in.config(bg='white', fg='black')
        self.girdSize_in.place(x=130, y=100)

        tip_lab1 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab1.place(x=240, y=15)
        Tooltip(tip_lab1, 'Enter the number of plants as a number of 1 to 16.')

        tip_lab2 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab2.place(x=240, y=55)
        Tooltip(tip_lab2, 'Enter the number of herbivores as a number of 0 to 15.')

        tip_lab3 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab3.place(x=240, y=105)
        Tooltip(tip_lab3, 'Enter the grid width as a number <= 80')

        start_btn = tk.Button(text='start', command=self.openSimualtor)
        start_btn.place(x=220, y=250)


    def openSimualtor(self):
        if self.numPlant_in.index('end') == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        elif self.numHerbi_in.index('end') == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        elif self.girdSize_in.index('end') == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        else:
            self.createSimWindow()
            self.toolbarElements()
            self.createTeams_labs('plants')
            self.createTeams_labs('herbivors')

    
    def inputValidation(self, inp, widgetName, minVal, maxVal):
        if inp == '':
            return True
        
        if inp.isdigit() and len(inp) <= 2:
            num = int(inp)
            minVal = int(minVal)
            maxVal = int(maxVal)

            if minVal <= num <= maxVal:
                return True
            
        widget = self.window.nametowidget(widgetName)
        widget.bell()
        messagebox.showwarning('Invalid Input', f'Please enter a number between {minVal} and {maxVal}.')
        widget = self.window.nametowidget(widgetName)
        self.window.after(0, lambda: widget.delete(0, tk.END))
        return False
    

    def createSimWindow(self):
        self.simWindow = tk.Tk()
        self.selectedBtn = tk.IntVar(self.simWindow) # zum Zurücksetzen
        self.simWindow.title('Simulator')
        self.simWindow.geometry(f'{self.screen_width}x{self.screen_height}')

        # Toolbar-Frame erstellen
        self.toolbar = tk.Frame(self.simWindow)
        self.toolbar.grid(row=0, column=0, columnspan=3, sticky='we')
        self.simWindow.grid_rowconfigure(0, weight=0)

        # Erstelle drei Rahmen (links, mitte, rechts)
        self.leftFrame = tk.Frame(self.simWindow, bg='lightblue')
        self.centerFrame = tk.Frame(self.simWindow)
        self.rightFrame = tk.Frame(self.simWindow, bg='lightblue')

        # Rahmen im Gitter anordnen (Zeile 1, da Zeile 0 für Toolbar reserviert ist)
        self.leftFrame.grid(row=1, column=0, sticky='nswe')
        self.centerFrame.grid(row=1, column=1, sticky='nswe')
        self.rightFrame.grid(row=1, column=2, sticky='nswe')

        # Spaltengewichte einstellen, um die Größe der Bereiche zu steuern
        self.simWindow.grid_columnconfigure(0, weight=1)  # Linker Bereich
        self.simWindow.grid_columnconfigure(1, weight=5)  # Mittlerer Bereich (größer)
        self.simWindow.grid_columnconfigure(2, weight=0)  # Rechter Bereich

        # Zeilengewicht einstellen, um die vertikale Dehnung zu ermöglichen
        self.simWindow.grid_rowconfigure(0, weight=0)  # Toolbar, kein Dehnen
        self.simWindow.grid_rowconfigure(1, weight=1)  # Hauptinhalt, dehnbar
        self.simWindow.grid_rowconfigure(2, weight=0)  # Untere Leiste, kein Dehnen

        self.bottonbar = tk.Frame(self.simWindow, height=15)
        self.bottonbar.grid(row=2, column=0, columnspan=3, sticky='we')

        self.createPlantsFrame()
        self.createHerbivorFrame()
        self.createBattlefield()
        
    def createTeams_labs(self, team):
        checkBtnList = []
        plants = int(self.numPlant_in.get())
        herbivors = int(self.numHerbi_in.get())
        
        if not hasattr(self, 'selectedBtn'):
            self.selectedBtn = tk.IntVar(self.simWindow)   
        
        if team == 'plants':
            
            for plantBtn in checkBtnList:
                plantBtn.destroy()

            checkBtnList.clear()

            for i in range(plants):
                newPlant = tk.Checkbutton(self.leftFrame, text=f'plant {i+1}', font=('Arial', 18), variable=self.selectedBtn, onvalue=i, offvalue=0)
                newPlant.grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
                checkBtnList.append(newPlant)
                
                newColor = tk.Label(self.leftFrame, text='   ', font=('Arial', 18), bg=self.colorList_p[i])
                newColor.grid(row=i+1, column=1, padx=10, pady=10, sticky='w') 
        
        elif team == 'herbivors':
           
            for herbivorBtn in checkBtnList:
                herbivorBtn.destroy()

            checkBtnList.clear()

            for i in range(herbivors):
                newHerbivor = tk.Checkbutton(self.rightFrame, text=f'herbivor {i+1}', font=('Arial', 18), variable=self.selectedBtn, onvalue=i+plants, offvalue=0)
                newHerbivor.grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
                checkBtnList.append(newHerbivor)

                newColor = tk.Label(self.rightFrame, text='   ', font=('Arial', 18), bg=self.colorList_h[i])
                newColor.grid(row=i+1, column=1, padx=10, pady=10, sticky='w')


    def createPlantsFrame(self):
        plantHeader = tk.Frame(self.leftFrame)
        plantHeader.grid(row=0, column=0, columnspan=2, sticky='nswe')

        self.leftFrame.grid_rowconfigure(0, weight=0)  # plantHeader nicht dehnbar in der Höhe
        self.leftFrame.grid_rowconfigure(1, weight=0)  # darunterliegende Zeile dehnbar
        self.leftFrame.grid_columnconfigure(1, weight=1)  # gesamte Breite nutzen

        plantsPara_lab = tk.Label(plantHeader, text='plants parameter', bg='blue', font=('Arial', 25))
        plantsPara_lab.grid(row=2, column=0, sticky='nswe')

        plantHeader.grid_rowconfigure(0, weight=1)
        plantHeader.grid_columnconfigure(0, weight=1)


    def createHerbivorFrame(self):
        # Header im rechten Bereich erstellen
        herbivoreHeader = tk.Frame(self.rightFrame)
        herbivoreHeader.grid(row=0, column=0, columnspan=2, sticky='nswe')

        self.rightFrame.grid_rowconfigure(0, weight=0)  
        self.rightFrame.grid_rowconfigure(1, weight=0)  
        self.rightFrame.grid_columnconfigure(1, weight=1)

        # Text im Header zentrieren
        herbivorePara_lab = tk.Label(herbivoreHeader, text='herbivores parameter', bg='purple', font=('Arial', 25))
        herbivorePara_lab.grid(row=0, column=0, sticky='nsew')

        # Konfiguration der Zeilen und Spalten im herbivoreHeader
        herbivoreHeader.grid_rowconfigure(0, weight=1)
        herbivoreHeader.grid_columnconfigure(0, weight=1)


    def createBattlefield(self):
        self.canvasContainer = tk.Frame(self.centerFrame)
        self.canvasContainer.pack(fill='both', expand=True)

        # Canvas für das Grid
        self.canvas = tk.Canvas(self.canvasContainer, bg='white', bd=1, relief='solid')
        self.canvas.pack(fill='both', expand=True)

        width = int(self.girdSize_in.get())
        height = int(self.girdSize_in.get())

        # Bereinige die Canvas vor dem Zeichnen
        self.canvas.delete('all')

        # Größe des Canvas berechnen
        self.canvas.update()  # Aktualisiere die Canvas-Größe
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()-30

        # Bestimme die Größe jedes Quadrats
        if width > 0 and height > 0:
            square_width = canvas_width / width
            square_height = canvas_height / height

            # Zeichne die Quadrate
            self.squares = {}
            for i in range(width):
                for j in range(height):
                    x1 = i * square_width
                    y1 = j * square_height
                    x2 = x1 + square_width
                    y2 = y1 + square_height
                    squareID = self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='white', width=2)
                    self.squares[squareID] = (x1, y1, x2, y2)

            self.canvas.bind('<Button-1>', self.onCanvasClick)
            

    def onCanvasClick(self, event):
        itm = self.canvas.find_closest(event.x, event.y)[0]
        plants = int(self.numPlant_in.get())
        herbivor = int(self.numHerbi_in.get())

        self.colors = []
        self.colors = self.colorList_p[:plants] + self.colorList_h[:herbivor]
        
        # Debug-Ausgaben zur Überprüfung
        print(f"Colors list length: {len(self.colors)}")
        print(f"Selected value: {self.selectedBtn.get()}")

        if itm in self.squares:
            if itm in self.selected_squares:
                self.canvas.itemconfig(itm, fill='white')
                self.selected_squares.remove(itm)
            else:
                selectedValue = self.selectedBtn.get()
                if 0 <= selectedValue < len(self.colors):
                    self.canvas.itemconfig(itm, fill=self.colors[selectedValue])
                    self.selected_squares.append(itm)
                else:
                    print(f"Index out of range: {selectedValue}")

    def toolbarElements(self):
        fileBtn = tk.Button(self.toolbar, text='save file', width=10, command=self.saveFile)
        fileBtn.grid(row=0, column=0, sticky='nswe')

        plotBtn = tk.Button(self.toolbar, text='plots', width=10)
        plotBtn.grid(row=0, column=1, sticky='nswe')

        simBtn = tk.Button(self.toolbar, text='simulation', width=10)
        simBtn.grid(row=0, column=2, sticky='nswe')

    def saveFile(self):
        filePath = filedialog.asksaveasfilename(title='select a location to save the file', defaultextension='.txt')

        print(filePath)


    def mainloop(self):
        self.window.mainloop()

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()