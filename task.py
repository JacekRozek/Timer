import tkinter as tk
from tkinter import Tk, Button, ttk, messagebox
from adds import *
import time


def submit_form():
    task = entry_field['task'].get()
    taks_time = entry_field['task_time'].get()
    
    messagebox.showinfo("Potwierdzenie", "Formularz został złożony!")

def logout():
    root.deiconify()  # Ponowne wyświetlenie okna logowania
    root.destroy()
    

##  ustawienia okna głównego
root = Tk()
root.title('Time Tracker')
root.geometry("400x400")
root.iconbitmap('./images/stopwatch.ico')
root.minsize(200, 150)
root.maxsize(1000, 800)

entry_field = {}

## panel "Witaj w TimeTracker!"
greeting = tk.Label(
    text= "Witaj w TimeTracker!",
    borderwidth= 1)
greeting.pack(
    padx=1,
    pady=10)


task = tk.Label(
    justify= tk.LEFT,
    text= "Czym będziesz się dzisiaj zajmować?",
    borderwidth= 1,
    height= 1,)
task.pack(
    anchor=tk.W,
    padx=5,
    pady=5,
)

entry_field['task'] = tk.Entry(
    justify=tk.LEFT,
    width=50)
entry_field['task'].pack()

task_time = tk.Label(
    justify= tk.LEFT,
    text= "Ile czasu przewidujesz na to zadanie?",
    borderwidth= 1,
    height= 1,)
task_time.pack(
    anchor=tk.W,
    padx=5,
    pady=5,
)

entry_field['task_time'] = tk.Entry(
    justify=tk.LEFT,
    width=5)
entry_field['task_time'].pack()

click_button = Button( 
    text="Start", 
    command=submit_form)
click_button.pack(
    anchor=tk.CENTER,
    padx=5,
    pady=5,
)

for field in entry_field.values():
    field.pack(anchor=tk.W, padx=5, pady=1, fill=tk.X)

logout_button = Button(
    root,
    text="Logout",
    command=lambda: root.logout())
logout_button.pack(
    anchor=tk.SE,
    padx=5,
    pady=5,
)

exit_button = Button(
    root,
    text="Quit",
    command=lambda: root.quit())
exit_button.pack(
    anchor=tk.SW,
    padx=5,
    pady=5,
)



root.mainloop()