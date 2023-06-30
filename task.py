import tkinter as tk
from tkinter import ttk, messagebox
# from adds import *
from stopwatch import *
import time
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from multiprocessing import Process, Queue


class TaskApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Time Tracker')
        self.root.geometry("400x225")
        self.root.iconbitmap('./images/stopwatch.ico')
        self.root.eval('tk::PlaceWindow . center')
        self.root.minsize(200, 150)
        self.root.maxsize(1000, 800)

        greeting = tk.Label(text="Witaj w TimeTracker!", borderwidth=1)
        greeting.pack(padx=1, pady=10)

        self.fields = {}
        self.fields['task_label'] = ttk.Label(text="Czym będziesz się dzisiaj zajmować?")
        self.fields['task'] = ttk.Entry()
        self.fields['task_time_label'] = ttk.Label(text="Ile czasu przewidujesz na to zadanie?")
        self.fields['task_time'] = ttk.Entry()
        self.fields['task_time'].bind('<Return>', self.on_enter)
        for field in self.fields.values():
            field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        
        self.logged_in = True
        self.last_activity_time = None
        self.inactivity_timeout = 4000  # 10 sekund
        
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady= 10)
        
        self.start_button = tk.Button(button_frame, text="Rozpocznij", command=self.submit_form)
        self.start_button.pack(side=tk.LEFT, padx=10)
        self.cancel_button = tk.Button(button_frame, text="Anuluj", command=self.cancel)
        self.cancel_button.pack(side=tk.LEFT, padx=10)
                
        ### Zabezpieczenie przed zamknięciem bez wylogowania
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def submit_form(self):
        task = self.fields['task'].get()
        task_time = self.fields['task_time'].get()
        # data_queue.put((task, task_time))  # Dodaj dane do kolejki
        # Przekazanie danych do klasy StopwatchApp
        self.root.deiconify() # Przywrócenie okna
        self.root.destroy()      
        stopwatch_app = StopwatchApp(task, task_time)
        stopwatch_app.start_stopwatch()

    def on_enter(self, event):
        self.login()

    def logout(self):
        self.logged_in = False
        self.root.deiconify() # Przywrócenie okna
        self.root.destroy()
        try:
            subprocess.run(['python', 'main.py'])  # Uruchomienie pliku 'main.py' w nowym procesie
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
    
    def cancel(self):
        self.root.deiconify() # Przywrócenie okna
        self.root.destroy()
        try:
            subprocess.run(['python', 'panel.py'])  # Uruchomienie pliku 'main.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'panel.py'")
    
            
if __name__ == "__main__": #plik jest uruchamiany automatycznie tylko w przypadku bezpośredniego uruchomienia
    app = TaskApp()