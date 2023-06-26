import tkinter as tk
from datetime import datetime
import time

class Stopwatch:
    def __init__(self, master):
        self.master = master
        self.master.title("Stoper")
        self.master.title('Time Tracker')
        self.master.geometry("175x100")
        self.master.attributes("-toolwindow", 1)
        self.master.iconbitmap('./images/stopwatch.ico')
        self.master.attributes("-topmost", True)
        self.master.minsize(175, 100)
        self.master.maxsize(300, 200)

        self.elapsed_time = 0
        self.is_running = False

        self.time_label = tk.Label(self.master, text="00:00:00", font=("Arial", 24))
        self.start_button = tk.Button(self.master, text="Start", command=self.start)
        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop)
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset)

        self.time_label.pack(pady=10)
        self.start_button.pack(pady=5)
        self.stop_button.pack(pady=5)
        self.reset_button.pack(pady=5)

        self.update_time()

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.update_time()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.elapsed_time += time.time() - self.start_time

    def reset(self):
        self.is_running = False
        self.elapsed_time = 0
        self.update_time()

    def update_time(self):
        if self.is_running:
            elapsed = self.elapsed_time + time.time() - self.start_time
        else:
            elapsed = self.elapsed_time

        hours = int(elapsed / 3600)
        minutes = int((elapsed % 3600) / 60)
        seconds = int(elapsed % 60)

        time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        self.time_label.config(text=time_string)

        self.master.after(1000, self.update_time)

window = tk.Tk() # Tworzenie głównego okna
stopwatch = Stopwatch(window)
# stopwatch_label = tk.Label(window, text="00:00:00", font=("Helvetica", 20))
# stopwatch_label.pack(pady=20)

window.mainloop()
