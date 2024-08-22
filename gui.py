
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

        girdWidth_lab = tk.Label(text='grid width')
        gridHeight_lab = tk.Label(text='grid height')
        girdWidth_lab.place(x=10, y=100)
        gridHeight_lab.place(x=10, y=140)

        # Validierungsfunktionen Grid
        valiGrid_in = (self.window.register(self.inputValidation), '%P', '%W', 1, 80)

        self.girdWidth_in = tk.Entry(width=10, validate='key', validatecommand=valiGrid_in)
        self.gridHeight_in = tk.Entry(width=10, validate='key', validatecommand=valiGrid_in)
        self.girdWidth_in.config(bg='white', fg='black')
        self.gridHeight_in.config(bg='white', fg='black')
        self.girdWidth_in.place(x=130, y=100)
        self.gridHeight_in.place(x=130, y=140)

        tip_lab1 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab1.place(x=240, y=15)
        Tooltip(tip_lab1, 'Enter the number of plants as a number of 1 to 16.')

        tip_lab2 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab2.place(x=240, y=55)
        Tooltip(tip_lab2, 'Enter the number of herbivores as a number of 0 to 15.')

        tip_lab3 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab3.place(x=240, y=105)
        Tooltip(tip_lab3, 'Enter the grid width as a number <= 80')

        tip_lab4 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab4.place(x=240, y=145)
        Tooltip(tip_lab4, 'Enter the grid heightas a number <= 80.')

        start_btn = tk.Button(text='start', command=self.openSimualtor)
        start_btn.place(x=220, y=250)

    def mainloop(self):
        self.window.mainloop()

    def openSimualtor(self):
        
        if self.numPlant_in.index("end") == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        elif self.numHerbi_in.index("end") == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        elif self.girdWidth_in.index("end") == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        elif self.gridHeight_in.index("end") == 0:
            messagebox.showwarning('Missing Input', 'Please enter a number')
        
        else:
            self.simWindow = tk.Tk()
            self.simWindow.title('Simulator')
            self.simWindow.geometry(f'{self.screen_width-100}x{self.screen_height-100}')



    def inputValidation(self, inp, widgetName, minVal, maxVal):
        
        if inp.isdigit():
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

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()