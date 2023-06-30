import tkinter as tk
import time
from tkinter import messagebox
import subprocess
from multiprocessing import Process, Queue
import sqlite3

class StopwatchApp:
    def __init__(self, task, task_time):
        self.root = tk.Tk()
        self.root.title('Stopwatch')
        self.root.geometry("250x150")
        
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.last_activity_time = None
        self.inactivity_timeout = 0
        
        goal = tk.Label(text=f"Pracujesz nad: {task}. Planujesz to zrobić w {task_time} ", borderwidth=1)
        goal.pack(padx=1, pady=10)
        
        self.label = tk.Label(self.root, text="00:00:00", font=("Arial", 24))
        self.label.pack(pady=20)
        
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_stopwatch)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.pause_button = tk.Button(button_frame, text="Pauza", command=self.pause_stopwatch, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=10)
        self.stop_button = tk.Button(button_frame, text="Stop", command=lambda: self.on_save(task, task_time), state=tk.NORMAL)

        self.stop_button.pack(side=tk.LEFT, padx=10)
        
        self.start_stopwatch()
        self.root.after(5000, self.check_inactivity)
        self.root.mainloop()
        
    def start_stopwatch(self):
        if not self.is_running:
            if self.start_time is None:
                self.start_time = time.time()
            else:
                self.start_time += time.time() - self.pause_time
            self.is_running = True
            self.update_stopwatch()
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            #self.root.after(5000, self.check_inactivity)
        
    def pause_stopwatch(self):
        if self.is_running:
            self.pause_time = time.time()
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
    
    def stop_stopwatch(self):
        self.pause_stopwatch()
        if self.is_running == False:
            self.start_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            saved_time = self.save_time()
            return saved_time
    
    def update_stopwatch(self):
        if self.is_running:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            self.elapsed_time = elapsed_time
            ### podział na godziny, minuty i sekundy
            hours = int(elapsed_time / 3600)
            minutes = int((elapsed_time % 3600) / 60)
            seconds = int(elapsed_time % 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}" # formatowalny string
            self.label.config(text=time_str)
        self.root.after(1, self.update_stopwatch)

    def save_time(self):
        if self.elapsed_time > 0:
            hours = int(self.elapsed_time / 3600)
            minutes = int((self.elapsed_time % 3600) / 60)
            seconds = int(self.elapsed_time % 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            return time_str
        else:
            return ""
            
    def on_save(self, task, task_time):
        time_saved = self.save_time()
        if time_saved:
            messagebox.showinfo("Zapisany czas", f"Zapisano czas: {time_saved}")
        else:
            messagebox.showinfo("Zapisany czas", "Nie zapisano żadnego czasu.")
        self.send_to_database(task, task_time, time_saved)
        self.root.deiconify()
        self.root.destroy()
        try:
            subprocess.run(['python', 'panel.py'])  # Uruchomienie pliku 'task.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'panel.py'")
    
    def write_to_file(self, elapsed_time):
        file_path = "czas_pracy.txt"
        with open(file_path, "a") as file:
           file.write(f"Czas pracy: {elapsed_time}\n")
    
    def send_to_database(self, task, task_time, time_saved):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        tab = [(task, task_time, time_saved)]
        cursor.executemany('INSERT INTO savedTimes (task, planned_time, time) VALUES (?, ?, ?)', tab)
        conn.commit()
        cursor.close()
        conn.close()
        self.write_to_file(tab)
    
    def logout(self):
        self.logged_in = False
        self.root.deiconify() # Przywrócenie okna
        self.root.destroy()
        try:
            subprocess.run(['python', 'main.py'])  # Uruchomienie pliku 'main.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'main.py'")
    
    def check_inactivity(self):
        current_time_var = tk.IntVar()
        current_time_var.set(int(time.time() * 1000))
        if  self.last_activity_time is None:
            self.last_activity_time = current_time_var.get()
        else:
            elapsed_time = current_time_var.get() - self.last_activity_time
            if elapsed_time >= self.inactivity_timeout:
                response = messagebox.askyesno("Potwierdzenie aktywności", "Czy jesteś nadal aktywny?")
                if response:
                    self.last_activity_time = current_time_var.get()
                else:
                    self.logout()
            else:
                self.last_activity_time = current_time_var.get() 
        self.root.after(5000, self.check_inactivity)
    
    
if __name__ == "__main__": #plik jest uruchamiany automatycznie tylko w przypadku bezpośredniego uruchomienia
    data_queue = Queue()
    StopwatchApp(data_queue)