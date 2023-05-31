import sqlite3

# Nawiązanie połączenia z bazą danych
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Utworzenie tabeli "users"
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL)''')

# Przykładowe dane użytkowników
users = [
    ('admin', 'admin'),
    ('user1', 'P@ssw0rd'),
    ('user2', 'P@ssw0rd')
]

# Wstawienie danych użytkowników do tabeli
cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

# Zatwierdzenie zmian i zamknięcie połączenia z bazą danych
conn.commit()
cursor.close()
conn.close()

print("Baza danych została wygenerowana i zapisana w pliku 'database.db'.")
