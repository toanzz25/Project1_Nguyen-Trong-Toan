import numpy as np
import time

class Measurement:
    def __init__(self, app):
        self.app = app

    def measure(self, f):
        try:
            if self.app.inst:
                self.app.inst.write(f"FREQ {f}")
                time.sleep(0.05)
                return float(self.app.inst.read())
            else:
                return np.random.random()
        except:
            return np.random.random()