import tkinter as tk
from tkinter import Tk, Button, ttk, messagebox
from adds import *
import time
import subprocess


class TimeTrackerApp:
    def __init__(self):
        ##  ustawienia okna głównego
        self.root = tk.Tk()
        self.root.title('Time Tracker')
        self.root.geometry("400x250")
        self.root.iconbitmap('./images/stopwatch.ico')
        self.root.minsize(200, 150)
        self.root.maxsize(1000, 800)

        greeting = tk.Label(text="Witaj w TimeTracker!", borderwidth=1)
        greeting.pack(padx=1, pady=10)

        ### Utworzenie pól formularza
        self.fields = {}
        self.fields['task_label'] = ttk.Label(text="Czym będziesz się dzisiaj zajmować?")
        self.fields['task'] = ttk.Entry()
        ###
        self.fields['task_time_label'] = ttk.Label(text="Ile czasu przewidujesz na to zadanie?")
        self.fields['task_time'].bind('<Return>', self.on_enter)
        ### Ustawianie dla każdego pola
        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        
        task = tk.Label(justify=tk.LEFT,
                        text="Czym będziesz się dzisiaj zajmować?",
                        borderwidth=1, height=1,)
        task.pack(anchor=tk.W, padx=5, pady=5)

        self.entry_field['task'] = tk.Entry(
            justify=tk.LEFT,
            width=50)
        self.entry_field['task'].pack()

        task_time = tk.Label(
            justify=tk.LEFT,
            text="Ile czasu przewidujesz na to zadanie?",
            borderwidth=1,
            height=1,)
        task_time.pack(
            anchor=tk.W,
            padx=5,
            pady=5,
        )

        self.entry_field['task_time'] = tk.Entry(
            justify=tk.LEFT,
            width=5)
        self.entry_field['task_time'].pack()

        click_button = Button(text="Start", command=self.submit_form)
        click_button.pack(anchor=tk.CENTER, padx=5, pady=5)

        for field in self.entry_field.values():
            field.pack(anchor=tk.W, padx=5, pady=1, fill=tk.X)

        logout_button = Button(
            self.root,
            text="Logout",
            command=self.logout)
        logout_button.pack(
            anchor=tk.SE,
            padx=5,
            pady=5,
        )

        exit_button = Button(
            self.root,
            text="Quit",
            command=self.root.quit)
        exit_button.pack(
            anchor=tk.SW,
            padx=5,
            pady=5,
        )

        self.root.mainloop()

    def submit_form(self):
        task = self.entry_field['task'].get()
        task_time = self.entry_field['task_time'].get()

        messagebox.showinfo("Potwierdzenie", "Formularz został złożony!")

    def logout(self):
        self.root.deiconify()  # Ponowne wyświetlenie okna logowania
        self.root.destroy()
        try:
            subprocess.run(['python', 'main.py'])  # Uruchomienie pliku 'task.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'main.py'")


app = TimeTrackerApp()
