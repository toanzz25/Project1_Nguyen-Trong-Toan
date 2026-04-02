import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyvisa
import threading
import time
import csv

class HP8903B_App:
    def __init__(self, root):
        self.root = root
        self.root.title("HP8903B Control Software")
        self.root.geometry("700x500")

        self.inst = None
        self.running = False

        # ====== CONNECTION ======
        frame_conn = tk.LabelFrame(root, text="Connection")
        frame_conn.pack(fill="x", padx=10, pady=5)

        self.addr = tk.Entry(frame_conn, width=25)
        self.addr.insert(0, "GPIB0::1::INSTR")
        self.addr.pack(side="left", padx=5)

        tk.Button(frame_conn, text="Connect", command=self.connect).pack(side="left")
        tk.Button(frame_conn, text="Disconnect", command=self.disconnect).pack(side="left")

        # ====== SETTING ======
        frame_set = tk.LabelFrame(root, text="Setting")
        frame_set.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_set, text="Frequency (Hz):").pack(side="left")
        self.freq = tk.Entry(frame_set, width=10)
        self.freq.insert(0, "1000")
        self.freq.pack(side="left", padx=5)

        tk.Button(frame_set, text="Set", command=self.set_freq).pack(side="left")

        # ====== MODE ======
        frame_mode = tk.LabelFrame(root, text="Measurement Mode")
        frame_mode.pack(fill="x", padx=10, pady=5)

        self.mode = ttk.Combobox(frame_mode, values=["Voltage", "THD", "Frequency"])
        self.mode.current(0)
        self.mode.pack(side="left", padx=5)

        tk.Button(frame_mode, text="Measure Once", command=self.measure_once).pack(side="left", padx=5)
        tk.Button(frame_mode, text="Start Realtime", command=self.start_realtime).pack(side="left", padx=5)
        tk.Button(frame_mode, text="Stop", command=self.stop_realtime).pack(side="left", padx=5)

        # ====== OUTPUT ======
        frame_out = tk.LabelFrame(root, text="Output")
        frame_out.pack(fill="both", expand=True, padx=10, pady=5)

        self.text = tk.Text(frame_out)
        self.text.pack(fill="both", expand=True)

        # ====== SAVE ======
        frame_save = tk.Frame(root)
        frame_save.pack(fill="x", padx=10, pady=5)

        tk.Button(frame_save, text="Save CSV", command=self.save_csv).pack(side="left")

        self.data_log = []

    # ====== CORE ======
    def log(self, msg):
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)

    def connect(self):
        try:
            rm = pyvisa.ResourceManager()
            self.inst = rm.open_resource(self.addr.get())
            self.log("Connected!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def disconnect(self):
        if self.inst:
            self.inst.close()
            self.inst = None
            self.log("Disconnected")

    def set_freq(self):
        try:
            f = self.freq.get()
            self.inst.write(f"FREQ {f}")
            self.log(f"Set Frequency: {f} Hz")
        except:
            self.log("Set frequency failed")

    def send_measure_cmd(self):
        mode = self.mode.get()

        if mode == "Voltage":
            self.inst.write("MEAS:VOLT?")
        elif mode == "THD":
            self.inst.write("MEAS:THD?")
        elif mode == "Frequency":
            self.inst.write("MEAS:FREQ?")

        return self.inst.read()

    def measure_once(self):
        try:
            value = self.send_measure_cmd()
            timestamp = time.strftime("%H:%M:%S")
            self.log(f"{timestamp} | {self.mode.get()} = {value}")
            self.data_log.append([timestamp, self.mode.get(), value])
        except:
            self.log("Measure error")

    # ====== REALTIME ======
    def realtime_loop(self):
        while self.running:
            try:
                value = self.send_measure_cmd()
                timestamp = time.strftime("%H:%M:%S")
                self.log(f"{timestamp} | {self.mode.get()} = {value}")
                self.data_log.append([timestamp, self.mode.get(), value])
                time.sleep(1)
            except:
                self.log("Realtime error")
                break

    def start_realtime(self):
        if not self.inst:
            self.log("Not connected!")
            return

        self.running = True
        threading.Thread(target=self.realtime_loop, daemon=True).start()
        self.log("Realtime started")

    def stop_realtime(self):
        self.running = False
        self.log("Realtime stopped")

    # ====== SAVE ======
    def save_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv")
        if file:
            with open(file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Mode", "Value"])
                writer.writerows(self.data_log)
            self.log("Saved to CSV")

# ====== RUN ======
if __name__ == "__main__":
    root = tk.Tk()
    app = HP8903B_App(root)
    root.mainloop()