import tkinter as tk
from tkinter import ttk, Button, messagebox
import sqlite3
import subprocess

def login():
    username = fields['username'].get()
    password = fields['password'].get()
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username=? AND password=?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    if user is not None:
        messagebox.showinfo("Sukces", "Zalogowano pomyślnie!")
        open_task_window()
        root.destroy()
    else:
        messagebox.showerror("Błąd", "Niepoprawne dane logowania!")
    

def on_enter(event):
    login()

def open_task_window():
    try:
        subprocess.run(['python', 'task.py'])  # Uruchomienie pliku 'task.py' w nowym procesie
    except FileNotFoundError:
        messagebox.showerror("Błąd", "Nie można znaleźć pliku 'task.py'")
        

# 
root = tk.Tk()
root.title('Time Tracker')
root.geometry("300x200")
root.iconbitmap('./images/stopwatch.ico')
root.minsize(200, 150)
root.maxsize(1000, 800)

greeting = tk.Label(
    text= "Witaj w TimeTracker!",
    borderwidth= 1)
greeting.pack(
    padx=1,
    pady=10)

fields = {}

fields['username_label'] = ttk.Label(text='Username:')
fields['username'] = ttk.Entry()

fields['password_label'] = ttk.Label(text='Password:')
fields['password'] = ttk.Entry(show="*")
fields['password'].bind('<Return>', on_enter)

for field in fields.values():
    field.pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)

ttk.Button(root, text='Login', command=login).pack(anchor=tk.W, padx=10, pady=5,)

root.mainloop()