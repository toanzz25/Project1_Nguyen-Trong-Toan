import csv, json
from tkinter import filedialog

class Data:
    def __init__(self, app):
        self.app = app

    def export(self):
        f = filedialog.asksaveasfilename(defaultextension=".csv")
        if not f:
            return
        with open(f, 'w', newline='') as file:
            w = csv.writer(file)
            w.writerow(["Freq","Val"])
            for i in range(len(self.app.freqs)):
                w.writerow([self.app.freqs[i], self.app.values[i]])

    def save(self):
        f = filedialog.asksaveasfilename(defaultextension=".json")
        if not f:
            return
        with open(f,'w') as file:
            json.dump({"freqs":self.app.freqs,"values":self.app.values}, file)

    def load(self):
        f = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not f:
            return
        with open(f) as file:
            d = json.load(file)
            self.app.freqs = d.get("freqs",[])
            self.app.values = d.get("values",[])
            self.app.ui.update_plot()