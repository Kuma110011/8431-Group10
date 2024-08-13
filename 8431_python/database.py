import sqlite3
import json
from user import User

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
                        introduction TEXT,
                        liked_users TEXT,
                        disliked_users TEXT,
                        matches TEXT,
                        attribute_weights TEXT)''')
    conn.commit()
    conn.close()

def add_user(username, password, name, age, gender, location, interests, introduction):
    conn = create_connection()
    cursor = conn.cursor()
    
    weights = {
            'age': 1.0,
            'gender_Male': 1.0,
            'gender_Female': 1.0,
            'location': 1.0,
            'introduction': 1.0}
    
    for interest in interests:
            weights[interest] = 1.0

    weights = json.dumps(weights)
    
    cursor.execute('''INSERT INTO users (username, password, name, age, gender, location, interests, introduction, attribute_weights)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                   (username, password, name, age, gender,location, ','.join(interests), introduction, weights))
    conn.commit()
    conn.close()

def get_user(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        user = User(*user_data[:-1]) #exclude attribute_weights for now
        weights = json.loads(user_data[-1]) #read the json string into dictionary
        user.assign_attribute_weights(weights)
        return user #return a User type
    
    return None

def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    all_users_data = cursor.fetchall()
    conn.close()
    
    all_users = []
    for user_data in all_users_data:
        user = User(*user_data[:-1]) 
        weights = json.loads(user_data[-1]) #read the json string into dictionary
        user.assign_attribute_weights(weights)
        all_users.append(user) #append the User object into the all_users list
        
    return all_users # list of User object

def delete_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users')
    all_users = cursor.fetchall()

    for user_data in all_users:
        # Adjust unpacking according to the actual number of columns
        if len(user_data) == 13:
            (current_user_id, username, password, name, age, gender, location, interests, introduction, liked_users, disliked_users, matches, extra_col) = user_data
        else:
            print("Unexpected number of columns:", len(user_data))
            continue
        
        liked_users_list = list(map(int, liked_users.split(','))) if liked_users else []
        disliked_users_list = list(map(int, disliked_users.split(','))) if disliked_users else []
        matches_list = list(map(int, matches.split(','))) if matches else []
        
        if user_id in liked_users_list:
            liked_users_list.remove(user_id)
        if user_id in disliked_users_list:
            disliked_users_list.remove(user_id)
        if user_id in matches_list:
            matches_list.remove(user_id)
        
        liked_users = ','.join(map(str, liked_users_list))
        disliked_users = ','.join(map(str, disliked_users_list))
        matches = ','.join(map(str, matches_list))
    
        cursor.execute('''
                       UPDATE users
                       SET liked_users = ?, disliked_users = ?, matches = ?
                       WHERE user_id = ?
                       ''', (liked_users, disliked_users, matches, current_user_id))
        
    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def update_user(user):
    conn = create_connection()
    cursor = conn.cursor()

    # Ensure there are no empty strings in the lists before joining
    liked_users = ','.join(filter(None, map(str, user.liked_users)))
    disliked_users = ','.join(filter(None, map(str, user.disliked_users)))
    matches = ','.join(filter(None, map(str, user.matches)))
    weights = json.dumps(user.get_attribute_weights())

    cursor.execute("""
        UPDATE users
        SET name = ?, age = ?, gender = ?, location = ?, interests = ?, introduction = ?, liked_users = ?, disliked_users = ?, matches = ?, attribute_weights = ?
        WHERE user_id = ?
    """, (user.name, user.age, user.gender, user.location, ','.join(user.interests), user.introduction, liked_users, 
          disliked_users, matches, weights, user.user_id))
    conn.commit()
    conn.close()
