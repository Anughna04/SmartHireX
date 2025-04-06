import sqlite3

def create_db():
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            match_score REAL,
            resume TEXT,
            email TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_candidate(name, match_score, resume,email):
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidates (name, match_score, resume, email) VALUES (?, ?, ?, ?)",
                (name, match_score, resume, email))
    conn.commit()
    conn.close()

def fetch_shortlisted(threshold=80):
    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, match_score, resume FROM candidates WHERE match_score >= ?", (threshold,))
    rows = cursor.fetchall()
    conn.close()
    return rows
