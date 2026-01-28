import sqlite3

conn = sqlite3.connect("bot.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    gold REAL DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount REAL,
    gold REAL,
    txid TEXT,
    screenshot TEXT,
    confirmed INTEGER DEFAULT 0,
    time TEXT
)
""")

conn.commit()
