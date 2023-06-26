import tkinter as tk
from tkinter import messagebox, ttk
import datetime
import sqlite3
import time
import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
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
        self.login_time = None

        self.login_button = tk.Button(self.root, text="Zaloguj", command=self.login)
        self.login_button.pack(pady=10)
        # self.logout_button = tk.Button(self.root, text="Wyloguj", command=self.logout, state=tk.DISABLED)
        # self.logout_button.pack(pady=10)

        ### Protokół zamykania okna
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
        try:
            subprocess.run(['python', 'test.py'])  # Uruchomienie pliku 'task.py' w nowym procesie
        except FileNotFoundError:
            messagebox.showerror("Błąd", "Nie można znaleźć pliku 'task.py'")
    
    def logout(self):
        if self.logged_in:
            self.logged_in = False
            logout_time = datetime.datetime.now()
            elapsed_time = logout_time - self.login_time
            self.send_email(elapsed_time)
            self.write_to_file(elapsed_time)
            self.login_button.config(state=tk.NORMAL)
            self.logout_button.config(state=tk.DISABLED)

    def check_activity(self):
        if self.logged_in:
            response = messagebox.askyesno("Potwierdzenie aktywności", "Czy jesteś nadal aktywny?")
            if response:
                self.root.after(3600000, self.check_activity)  # Sprawdź co 1 godzinę (3600000 ms)
            else:
                self.logout()

    def write_to_file(self, elapsed_time):
        file_path = "czas_pracy.txt"
        with open(file_path, "a") as file:
            file.write(f"Czas pracy: {elapsed_time}\n")

    # def send_email(self, elapsed_time):
    #     email_from = "your_email@example.com"
    #     email_to = "manager@example.com"
    #     smtp_server = "smtp.example.com"
    #     smtp_port = 587
    #     username = "your_email@example.com"
    #     password = "your_password"

    #     message = MIMEMultipart()
    #     message["From"] = email_from
    #     message["To"] = email_to
    #     message["Subject"] = "Czas pracy użytkownika"

    #     body = f"Czas pracy użytkownika: {elapsed_time}"
    #     message.attach(MIMEText(body, "plain"))

    #     with smtplib.SMTP(smtp_server, smtp_port) as server:
    #         server.starttls()
    #         server.login(username, password)
    #         server.sendmail(email_from, email_to, message.as_string())

    def on_closing(self):
        if self.logged_in:
            messagebox.showinfo("Informacja", "Najpierw wyloguj się przed zamknięciem aplikacji.")
        else:
            self.root.destroy()


if __name__ == "__main__":
    app = TimeTrackerApp()
    app.root.mainloop()
