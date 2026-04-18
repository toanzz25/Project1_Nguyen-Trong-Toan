import numpy as np
from tkinter import messagebox

class Sweep:
    def __init__(self, app):
        self.app = app

    def run(self):
        try:
            s = float(self.app.ui.start.get())
            e = float(self.app.ui.stop.get())
            n = int(self.app.ui.points.get())

            if s <= 0:
                messagebox.showerror("Error", "Start > 0")
                self.app.running = False
                return

            self.app.freqs = []
            self.app.values = []

            if self.app.ui.mode.get() == "Log":
                freqs = np.logspace(np.log10(s), np.log10(e), n)
            else:
                freqs = np.linspace(s, e, n)

            for f in freqs:
                if not self.app.running:
                    break

                val = self.app.measurement.measure(f)

                self.app.freqs.append(f)
                self.app.values.append(val)

                self.app.ui.update_plot()

            self.app.overlays.append((self.app.freqs.copy(), self.app.values.copy()))

        except Exception as ex:
            messagebox.showerror("Error", str(ex))

        self.app.running = False