import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT
)
""")

conn.commit()


def add_user(user_id, username, first_name):
    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id, username, first_name) VALUES(?,?,?)",
        (user_id, username, first_name)
    )
    conn.commit()


def get_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )
    return cursor.fetchone()
