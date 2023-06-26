import tkinter as tk
from tkinter import Tk, Button, ttk, messagebox
from adds import *
import datetime
import time
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class TimeTrackerApp:
    def __init__(self):
        ##  ustawienia okna głównego
        self.root = tk.Tk()
        self.root.title('Time Tracker')
        self.root.geometry("400x275")
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
        self.fields['task_time'] = ttk.Entry()
        self.fields['task_time'].bind('<Return>', self.on_enter)
        ### Ustawianie dla każdego pola
        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        ### Ustawienie znacznika, że użytkownik jest zalogowany
        self.logged_in = True
        self.last_activity_time = None
        self.inactivity_timeout = 4000  # 10 sekund
        
        
        self.buttons = {}
        self.start_button = Button(text="Start", command=self.submit_form)
        self.start_button.pack(anchor=tk.CENTER, padx=5, pady=5)
        
        self.logout_button = Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(anchor=tk.SE, padx=5, pady=5)

        self.exit_button = Button(self.root, text="Quit", command=self.on_closing)
        self.exit_button.pack(anchor=tk.SW, padx=5, pady=5)
        ### Nieaktywność
        self.root.after(1000, self.check_inactivity)
        
        ### Zabezpieczenie przed zamknięciem bez wylogowania
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def submit_form(self):
        task = self.fields['task'].get()
        task_time = self.fields['task_time'].get()

        messagebox.showinfo("Potwierdzenie", "Formularz został złożony!")

    def on_enter(self, event):
        self.login()

    def logout(self):
        self.logged_in = False
        self.root.deiconify() # Przywrócenie okna
        self.root.destroy()
        try:
            subprocess.run(['python', 'main.py'])  # Uruchomienie pliku 'task.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'main.py'")

    def on_closing(self):
        if self.logged_in:
            messagebox.showinfo("Informacja", "Najpierw wyloguj się przed zamknięciem aplikacji.")
        else:
            self.root.destroy()
    
    def write_to_file(self, elapsed_time):
        file_path = "czas_pracy.txt"
        with open(file_path, "a") as file:
            file.write(f"Czas pracy: {elapsed_time}\n")
    
    def send_email(self, elapsed_time):
        email_from = "your_email@example.com"
        email_to = "manager@example.com"
        smtp_server = "smtp.example.com"
        smtp_port = 587
        username = "your_email@example.com"
        password = "your_password"

        message = MIMEMultipart()
        message["From"] = email_from
        message["To"] = email_to
        message["Subject"] = "Czas pracy użytkownika"

        body = f"Czas pracy użytkownika: {elapsed_time}"
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.sendmail(email_from, email_to, message.as_string())
    
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
        
        self.root.after(1000, self.check_inactivity)

app = TimeTrackerApp()