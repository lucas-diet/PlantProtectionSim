
import tkinter as tk

class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Configuration')
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        window_width = 300
        window_height = 300

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2) - 200
        
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        numPlant_lab = tk.Label(text='number plants')
        numherbi_lab = tk.Label(text='number herbivores')
        numPlant_lab.place(x=10, y=10)
        numherbi_lab.place(x=10, y=50)

        numPlant_in = tk.Entry(width=10)
        numHerbi_in = tk.Entry( width=10)
        numPlant_in.config(bg='white', fg='black')
        numHerbi_in.config(bg='white', fg='black')
        numPlant_in.place(x=130, y=10)
        numHerbi_in.place(x=130, y=50)

        girdWidth_lab = tk.Label(text='grid width')
        gridHeight_lab = tk.Label(text='grid height')
        girdWidth_lab.place(x=10, y=100)
        gridHeight_lab.place(x=10, y=140)

        girdWidth_in = tk.Entry(width=10)
        gridHeight_in = tk.Entry(width=10)
        girdWidth_in.config(bg='white', fg='black')
        gridHeight_in.config(bg='white', fg='black')
        girdWidth_in.place(x=130, y=100)
        gridHeight_in.place(x=130, y=140)

        tip_lab1 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab1.place(x=240, y=15)

        tip_lab2 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab2.place(x=240, y=55)

        tip_lab3 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab3.place(x=240, y=105)

        tip_lab4 = tk.Label(text='?', borderwidth=1, relief='solid')
        tip_lab4.place(x=240, y=145)

    def mainloop(self):
        self.window.mainloop()



  
if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()