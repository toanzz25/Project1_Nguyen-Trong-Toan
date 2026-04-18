import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class UI:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        self.root.title("HP8903B PRO LAB")
        self.root.geometry("1300x750")

        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TLabel", padding=4)

        self.create_ui()

    def create_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        self.left_frame = ttk.Frame(main_frame, padding=15)
        self.left_frame.pack(side="left", fill="y")

        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.build_control()
        self.build_graph()

    def build_control(self):
        f = self.left_frame

        ttk.Label(f, text="Sweep Settings", font=("Segoe UI", 12, "bold")).pack(pady=10)

        grid_frame = ttk.Frame(f)
        grid_frame.pack()

        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        self.start = ttk.Entry(grid_frame); self.start.insert(0, "100")
        self.stop = ttk.Entry(grid_frame); self.stop.insert(0, "10000")
        self.points = ttk.Entry(grid_frame); self.points.insert(0, "50")

        ttk.Label(grid_frame, text="Start (Hz)").grid(row=0, column=0)
        self.start.grid(row=0, column=1)

        ttk.Label(grid_frame, text="Stop (Hz)").grid(row=1, column=0)
        self.stop.grid(row=1, column=1)

        ttk.Label(grid_frame, text="Points").grid(row=2, column=0)
        self.points.grid(row=2, column=1)

        self.mode = ttk.Combobox(grid_frame, values=["Linear", "Log"])
        self.mode.current(1)
        self.mode.grid(row=3, column=1)

        btn = ttk.Frame(f)
        btn.pack(pady=10, fill="x")

        ttk.Button(btn, text="Start", command=self.app.start).pack(fill="x")
        ttk.Button(btn, text="Stop", command=self.app.stop).pack(fill="x")
        ttk.Button(btn, text="Export", command=self.app.export).pack(fill="x")

    def build_graph(self):
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.cursor_label = ttk.Label(self.right_frame, text="Cursor:")
        self.cursor_label.pack()

        self.canvas.mpl_connect("motion_notify_event", self.on_cursor)

    def update_plot(self):
        self.ax1.clear()
        self.ax2.clear()

        for f, v in self.app.overlays:
            self.ax1.plot(f, 20*np.log10(np.maximum(v,1e-9)), alpha=0.3)

        if self.app.values:
            mag = 20*np.log10(np.maximum(self.app.values,1e-9))
            self.ax1.plot(self.app.freqs, mag)

        self.ax1.set_xscale("log")

        if len(self.app.values) > 1:
            phase = np.gradient(self.app.values)
        else:
            phase = [0]*len(self.app.values)

        if self.app.values:
            self.ax2.plot(self.app.freqs, phase)

        self.ax2.set_xscale("log")
        self.canvas.draw_idle()

    def on_cursor(self, event):
        if event.xdata:
            self.cursor_label.config(text=f"{event.xdata:.2f} Hz")