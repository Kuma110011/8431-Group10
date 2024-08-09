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
                        interests TEXT,
                        liked_users TEXT,
                        disliked_users TEXT,
                        matches TEXT)''')
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

def get_users():
    """Get all users from the database server"""
    
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()
    conn.close()
    return all_users

def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    
    # cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    
    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()

    for user_data in all_users:
        current_user_id, name, age, gender, location, interests, liked_users, disliked_users, matches = user_data
        
        liked_users_list = list(map(int, liked_users.split(','))) if liked_users else []
        disliked_users_list = list(map(int, disliked_users.split(','))) if disliked_users else []
        matches_list = list(map(int, matches.split(','))) if matches else []
        
        if user_id in liked_users_list:
            liked_users_list.remove(user_id)
        if user_id in disliked_users_list:
            disliked_users_list.remove(user_id)
        if user_id in matches_list:
            matches_list.remove(user_id)
        
        # update the current user with the modified lists
        liked_users = ','.join(map(str, liked_users_list))
        disliked_users = ','.join(map(str, disliked_users_list))
        matches = ','.join(map(str, matches_list))
    
        cursor.execute('''
                       UPDATE users
                       SET liked_users = ?, disliked_users = ?, matches = ?
                       WHERE user_id = ?
                       ''', (liked_users, disliked_users, matches, current_user_id))
        
        # delete the user from the database
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    
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