import tkinter as tk
import time

class Stopwatch:
    def __init__(self, master):
        self.master = master
        self.master.title("Stoper")

        self.elapsed_time = 0
        self.is_running = False

        self.time_label = tk.Label(self.master, text="00:00:00", font=("Arial", 24))
        self.start_button = tk.Button(self.master, text="Start", command=self.start_stopwatch)
        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_stopwatch)
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_stopwatch)

        self.time_label.pack(pady=10)
        self.start_button.pack(pady=5)
        self.stop_button.pack(pady=5)
        self.reset_button.pack(pady=5)

        self.update_time()

    def start_stopwatch(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time()
            self.update_time()

    def stop_stopwatch(self):
        if self.is_running:
            self.is_running = False
            self.elapsed_time += time.time() - self.start_time

    def reset_stopwatch(self):
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

root = tk.Tk()
stopwatch = Stopwatch(root)
root.mainloop()
