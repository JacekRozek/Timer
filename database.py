import sqlite3

# Nawiązanie połączenia z bazą danych
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL)''')

users = [
    ('admin', 'admin'),
    ('MStrach', 'P@ssw0rd'),
    ('JRozek', 'P@ssw0rd')
]

cursor.execute('''CREATE TABLE IF NOT EXISTS savedTimes
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task TEXT NOT NULL,
                  planned_time TEXT NOT NULL,
                  time TEXT NOT NULL)''')

savedTimes = [
    ('test', '00:01:00', '00:00:05')
]

# Wstawienie danych użytkowników do tabeli
cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)
cursor.executemany('INSERT INTO savedTimes (task, planned_time, time) VALUES (?, ?, ?)', savedTimes)

# Zatwierdzenie zmian i zamknięcie połączenia z bazą danych
conn.commit()
cursor.close()
conn.close()

print("Baza danych została wygenerowana i zapisana w pliku 'database.db'.")
