# database.py
# test-fabiola
import sqlite3

def create_connection():
    conn = sqlite3.connect('matching_app.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        name TEXT NOT NULL,
                        age INTEGER,
                        gender TEXT,
                        location TEXT,
                        interests TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password, name, age, gender, location, interests):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (username, password, name, age, gender, location, interests)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (username, password, name, age, gender, location, ','.join(interests)))
    conn.commit()
    conn.close()

def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def delete_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

def update_user(user):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET name = ?, age = ?, gender = ?, location = ?, interests = ?
        WHERE username = ?
    """, (user.name, user.age, user.gender, user.location, ','.join(user.interests), user.user_id))
    conn.commit()
    conn.close()