import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import subprocess

class TimeTrackerApp:
    def __init__(self):
        ### Opis wyglądu okna
        self.root = tk.Tk()
        self.root.title('Time Tracker')
        self.root.geometry("300x200")
        self.root.iconbitmap('./images/stopwatch.ico')
        self.root.minsize(200, 150)
        self.root.maxsize(1000, 800)
        
        greeting = tk.Label(text= "Witaj w TimeTracker!", borderwidth= 1)
        greeting.pack(padx=1, pady=10)

        ### Utowrzenie pól do wprowadzania danych logowania
        self.fields = {}
        self.fields['username_label'] = ttk.Label(text='Username:')
        self.fields['username'] = ttk.Entry()
        ###
        self.fields['password_label'] = ttk.Label(text='Password:')
        self.fields['password'] = ttk.Entry(show="*")
        self.fields['password'].bind('<Return>', self.on_enter)
        ### Ustawianie dla każdego pola
        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        
        self.logged_in = False

        self.login_button = tk.Button(self.root, text="Zaloguj", command=self.login)
        self.login_button.pack(pady=10)
        
        self.root.protocol("WM_DELETE_WINDOW") ### Protokół zamykania okna

    def login(self):
        username = self.fields['username'].get()
        password = self.fields['password'].get()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=? AND password=?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user is not None:
            messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
            self.open_task_window()
            self.root.destroy()
        else:
            messagebox.showerror("Błąd", "Niepoprawne dane logowania!")

    def on_enter(self, event):
        self.login()
    
    def open_task_window(self):
        self.root.deiconify()
        self.root.destroy()
        try:
            subprocess.run(['python', 'task.py'])  # Uruchomienie pliku 'task.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'task.py'")
    
    def on_closing(self):
            result = messagebox.askokcancel("Quit", "Czy na pewno chcesz zamknąć aplikację?")
            if result:
                self.root.destroy()


if __name__ == "__main__":
    app = TimeTrackerApp()
    app.root.mainloop()
