import tkinter as tk
from datetime import datetime

def update_clock():
    current_time = datetime.now().strftime("%H:%M:%S")
    label_time.config(text=current_time)
    label_time.after(1000, update_clock)  # Aktualizacja co 1000 ms

def move_window(event):
    window.geometry(f"+{event.x_root}+{event.y_root}")

# Tworzenie głównego okna
window = tk.Tk()
window.title('Current time')
window.overrideredirect(True)
window.geometry("105x75")
window.attributes("-toolwindow", 1)
window.iconbitmap('./images/stopwatch.ico')
window.minsize(105, 75)
window.maxsize(200, 100)
window.bind("<B1-Motion>", move_window)


# Tworzenie etykiety zegara
label_time = tk.Label(window, text="", font=("Helvetica", 20))
label_time.pack(pady=20)

close_button = tk.Button(window, text="X", command=window.quit)
close_button.pack()

# Rozpoczęcie aktualizacji zegara
update_clock()

# Uruchomienie pętli głównej okna
window.mainloop()
