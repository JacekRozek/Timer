import tkinter as tk
from datetime import datetime
import time

class Stopwatch:
    def __init__(self):
        self.is_running = False
        self.start_time = None

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.now()
            self.update()

    def stop(self):
        if self.is_running:
            self.is_running = False

    def reset(self):
        self.is_running = False
        self.start_time = None
        self.label.config(text="00:00:00")

    def update(self):
        if self.is_running:
            elapsed_time = datetime.now() - self.start_time
            elapsed_time_str = str(elapsed_time).split(".")[0]
            self.label.config(text=elapsed_time_str)
            self.label.after(100, self.update)  # Aktualizacja co 100 ms
    
def move_window(event):
    window.geometry(f"+{event.x_root}+{event.y_root}")

# Powiązanie zdarzenia przemieszczania okna z funkcją

# Tworzenie głównego okna
window = tk.Tk()
window.title('Time Tracker')
window.geometry("175x100")
window.attributes("-toolwindow", 1)
window.iconbitmap('./images/stopwatch.ico')
window.attributes("-topmost", True)
window.overrideredirect(True)
window.minsize(50, 20)
window.maxsize(200, 100)

close_button = tk.Button(window, text="X", command=window.quit)
close_button.pack()

window.bind("<B1-Motion>", move_window)

# Tworzenie etykiety z czasem
stopwatch = Stopwatch()
stopwatch_label = tk.Label(window, text="00:00:00", font=("Helvetica", 20))
stopwatch_label.pack(pady=20)

# Tworzenie przycisków
start_button = tk.Button(window, text="Start", command=stopwatch.start)
start_button.pack(side=tk.LEFT, padx=10)
stop_button = tk.Button(window, text="Stop", command=stopwatch.stop)
stop_button.pack(side=tk.LEFT, padx=10)
reset_button = tk.Button(window, text="Reset", command=stopwatch.reset)
reset_button.pack(side=tk.LEFT, padx=10)

# Uruchomienie pętli głównej okna
window.mainloop()
