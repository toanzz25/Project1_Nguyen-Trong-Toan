import threading

class Control:
    def __init__(self, app):
        self.app = app

    def start(self):
        if self.app.running:
            return
        self.app.running = True
        threading.Thread(target=self.app.sweep_worker, daemon=True).start()

    def stop(self):
        self.app.running = False