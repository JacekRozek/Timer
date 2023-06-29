import tkinter as tk
from tkinter import messagebox
import sqlite3
import time
import subprocess


class SavedTimesList:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Time Tracker')
        self.root.geometry("400x300")
        self.root.iconbitmap('./images/stopwatch.ico')
        self.root.eval('tk::PlaceWindow . center')
        self.root.minsize(200, 150)
        self.root.maxsize(1000, 800)
        
        self.logged_in = True

        self.greeting = tk.Label(text="Historia zapisanych zadań", borderwidth=1)
        self.greeting.pack(padx=1, pady=10)
        self.listbox = tk.Listbox(self.root, width=100)
        self.listbox.pack(padx=10, pady=10)
        ### Panel z przyciskami
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        self.add_button = tk.Button(button_frame, text="Dodaj", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=10)
        
        self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.load_saved_times()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def load_saved_times(self):
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM savedTimes")
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                self.listbox.insert(tk.END, f"#{row[0]} | Task: {row[1]} | Planned Time: {row[2]} | Actual Time: {row[3]}")
        except sqlite3.Error as e:
            print(f"Error retrieving saved times: {e}")

    def logout(self):
        self.logged_in = False
        self.root.deiconify() # Przywrócenie okna
        self.root.destroy()
        try:
            subprocess.run(['python', 'main.py'])  # Uruchomienie pliku 'main.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'main.py'")
    
    def add_task(self):
        self.root.deiconify() # Przywrócenie okna
        self.root.destroy()
        try:
            subprocess.run(['python', 'task.py'])  # Uruchomienie pliku 'main.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'main.py'")
    
    def cancel(self):
        self.root.deiconify()
        self.root.destroy()
        try:
            subprocess.run(['python', 'panel.py'])  # Uruchomienie pliku 'task.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'panel.py'")
    
    def on_closing(self):
        if self.logged_in:
            messagebox.showinfo("Informacja", "Najpierw wyloguj się przed zamknięciem aplikacji.")
        else:
            self.root.destroy()

if __name__ == "__main__": #plik jest uruchamiany automatycznie tylko w przypadku bezpośredniego uruchomienia
    app = SavedTimesList()