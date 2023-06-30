import tkinter as tk
import time
from tkinter import messagebox
import subprocess
from multiprocessing import Process, Queue
import sqlite3


class WarningApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Potwierdź aktywność')
        self.root.geometry("200x125")
        self.root.iconbitmap('./images/stopwatch.ico')
        self.root.eval('tk::PlaceWindow . center')
        self.root.minsize(200, 150)
        
        self.elapsed_time = 0
        self.inactivity_timeout = 5
        self.last_activity_time = None
        
        self.start_button = tk.Button(text="Start", command=self.count_time)
        self.start_button.pack(side=tk.LEFT, padx=10)
                
        self.root.mainloop()
        # return self.count_time()
    
    def count_time(self):
        time.sleep(5)
        current_time_var = tk.IntVar()
        current_time_var.set(int(time.time() * 1000))
        if  self.last_activity_time is None:
            self.last_activity_time = current_time_var.get()
        else:
            elapsed_time = current_time_var.get() - self.last_activity_time
            if elapsed_time >= self.inactivity_timeout:
                return False
            else:
                return True
        self.root.deiconify() # Przywrócenie okna
        self.root.destroy()