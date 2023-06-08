import tkinter as tk

# Tworzenie głównego okna
window = tk.Tk()
window.overrideredirect(True)  # Usunięcie obramowania i paska tytułowego
window.geometry("300x200")  # Ustawienie rozmiaru okna
window.attributes("-topmost", True)

# Funkcja do przechwytywania przemieszczania okna
def move_window(event):
    window.geometry(f"+{event.x_root}+{event.y_root}")

# Powiązanie zdarzenia przemieszczania okna z funkcją
window.bind("<B1-Motion>", move_window)

# Uruchomienie pętli głównej okna
window.mainloop()
