
import tkinter as tk

class Tooltip:

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.showTooltip)
        self.widget.bind("<Leave>", self.hideTooltip)

    def showTooltip(self, event):
        x = event.x_root + 10
        y = event.y_root + 10
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f'+{x}+{y}')
        label = tk.Label(self.tooltip, text=self.text, bg='yellow', fg='black', relief='solid', borderwidth=1)
        label.pack()
        
    def hideTooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None