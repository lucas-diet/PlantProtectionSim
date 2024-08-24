
import tkinter as tk
from tkinter import messagebox

from tooltip import Tooltip

class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Initital Configuration')
        
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        window_width = 300
        window_height = 300

        center_x = int(self.screen_width / 2 - window_width / 2)
        center_y = int(self.screen_height / 2 - window_height / 2) - 200
        
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.createInitWindow()

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

        girdWidth_lab = tk.Label(text='grid size')
        #gridHeight_lab = tk.Label(text='grid height')
        girdWidth_lab.place(x=10, y=100)
        #gridHeight_lab.place(x=10, y=140)

        # Validierungsfunktionen Grid
        valiGrid_in = (self.window.register(self.inputValidation), '%P', '%W', 1, 80)

        self.girdSize_in = tk.Entry(width=10, validate='key', validatecommand=valiGrid_in)
        #self.gridHeight_in = tk.Entry(width=10, validate='key', validatecommand=valiGrid_in)
        self.girdSize_in.config(bg='white', fg='black')
        #self.gridHeight_in.config(bg='white', fg='black')
        self.girdSize_in.place(x=130, y=100)
        #self.gridHeight_in.place(x=130, y=140)

        tip_lab1 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab1.place(x=240, y=15)
        Tooltip(tip_lab1, 'Enter the number of plants as a number of 1 to 16.')

        tip_lab2 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab2.place(x=240, y=55)
        Tooltip(tip_lab2, 'Enter the number of herbivores as a number of 0 to 15.')

        tip_lab3 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab3.place(x=240, y=105)
        Tooltip(tip_lab3, 'Enter the grid width as a number <= 80')

        #tip_lab4 = tk.Label(text='?', borderwidth=1, relief='solid')
        #tip_lab4.place(x=240, y=145)
        #Tooltip(tip_lab4, 'Enter the grid heightas a number <= 80.')

        start_btn = tk.Button(text='start', command=self.openSimualtor)
        start_btn.place(x=220, y=250)


    def openSimualtor(self):
        
        if self.numPlant_in.index('end') == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        elif self.numHerbi_in.index('end') == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        elif self.girdSize_in.index('end') == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        #elif self.gridHeight_in.index('end') == 0:
            #messagebox.showwarning('Missing Input', 'Please enter a number')
        
        else:
            self.createSimWindow()
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
        self.simWindow.title('Simulator')
        self.simWindow.geometry(f'{self.screen_width-100}x{self.screen_height-100}')

        # Toolbar-Frame erstellen
        toolbar = tk.Frame(self.simWindow, bg='white', height=25)
        toolbar.grid(row=0, column=0, columnspan=3, sticky='we')

        # Erstelle drei Rahmen (links, mitte, rechts)
        self.leftFrame = tk.Frame(self.simWindow, bg='green')
        self.centerFrame = tk.Frame(self.simWindow)
        self.rightFrame = tk.Frame(self.simWindow, bg='red')

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

        self.createPlantsFrame()
        self.createHerbivorFrame()
        self.createBattlefield()

            
    def createTeams_labs(self, team):
        checkBtnList = []

        if team == 'plants':
            plants = int(self.numPlant_in.get())

            for plantLabel in checkBtnList:
                plantLabel.destroy()
            checkBtnList.clear()

            for i in range(plants):
                newPlant = tk.Checkbutton(self.leftFrame, text=f'plant {i+1}', font=('Arial', 18))
                newPlant.grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
                checkBtnList.append(newPlant)
        
        elif team == 'herbivors':
            herbivors = int(self.numHerbi_in.get())

            for herbivorLabel in checkBtnList:
                herbivorLabel.destroy()
            checkBtnList.clear()

            for i in range(herbivors):
                newHerbivor = tk.Checkbutton(self.rightFrame, text=f'herbivor {i+1}', font=('Arial', 18))
                newHerbivor.grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
                checkBtnList.append(newHerbivor)


    def createPlantsFrame(self):
        plantHeader = tk.Frame(self.leftFrame)
        plantHeader.grid(row=0, column=0, sticky='nswe')

        self.leftFrame.grid_rowconfigure(0, weight=0)  # plantHeader nicht dehnbar in der Höhe
        self.leftFrame.grid_rowconfigure(1, weight=0)  # darunterliegende Zeile dehnbar
        self.leftFrame.grid_columnconfigure(0, weight=1)  # gesamte Breite nutzen

        plantsPara_lab = tk.Label(plantHeader, text='plants parameter', bg='blue', font=('Arial', 25))
        plantsPara_lab.grid(row=2, column=0, sticky='nswe')

        plantHeader.grid_rowconfigure(0, weight=1)
        plantHeader.grid_columnconfigure(0, weight=1)


    def createHerbivorFrame(self):
        # Header im rechten Bereich erstellen
        herbivoreHeader = tk.Frame(self.rightFrame)
        herbivoreHeader.grid(row=0, column=0, sticky='nswe')

        self.rightFrame.grid_rowconfigure(0, weight=0)  
        self.rightFrame.grid_rowconfigure(1, weight=0)  
        self.rightFrame.grid_columnconfigure(0, weight=1)

        # Text im Header zentrieren
        herbivorePara_lab = tk.Label(herbivoreHeader, text='herbivores parameter', bg='purple', font=('Arial', 25))
        herbivorePara_lab.grid(row=0, column=0, sticky='nsew')

        # Konfiguration der Zeilen und Spalten im herbivoreHeader
        herbivoreHeader.grid_rowconfigure(0, weight=1)
        herbivoreHeader.grid_columnconfigure(0, weight=1)


    def createBattlefield(self):

        # Canvas für das Grid
        self.canvas = tk.Canvas(self.centerFrame, bg='white')
        self.canvas.pack(fill='both', expand=True)

        width = int(self.girdSize_in.get())
        height = int(self.girdSize_in.get())

        # Bereinige die Canvas vor dem Zeichnen
        self.canvas.delete('all')

        # Größe des Canvas berechnen
        self.canvas.update()  # Aktualisiere die Canvas-Größe
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

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
                    squareID = self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill='white', width=3)
                    self.squares[squareID] = (x1, y1, x2, y2)

            self.canvas.bind('<Button-1>', self.onCanvasClick)
            

    def onCanvasClick(self, event):
        itm = self.canvas.find_closest(event.x, event.y)[0]

        if itm in self.squares:
            if itm in self.selected_squares:
                self.canvas.itemconfig(itm, fill='white')
                self.selected_squares.remove(itm)
            else:
                self.canvas.itemconfig(itm, fill='blue')
                self.selected_squares.append(itm)

    def mainloop(self):
        self.window.mainloop()

if __name__ == '__main__':
    gui = GUI()
    gui.mainloop()