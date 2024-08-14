#an optional file to reset database matching_app.db
#clean_database() function delete matching_app.db
#create_dummy_users() create dummy users into the database

import os
import sqlite3
from database import create_tables, add_user

def clean_database(db_name='matching_app.db'):
    """Deletes the specified database file to reset the database."""
    if os.path.exists(db_name):
        try:
            os.remove(db_name)
            print(f"Database '{db_name}' has been deleted successfully.")
        except Exception as e:
            print(f"An error occurred while trying to delete the database: {e}")
    else:
        print(f"Database '{db_name}' does not exist.")

def create_dummy_users():
    """Creates and inserts dummy users into the database one by one."""
    # Password is the same for all users
    password = "123"

    # Define each user's attributes manually
    users = [
        {"username": "user1", "name": "John", "age": 25, "gender": "Male", "location": "Toronto", "interests": ["Music", "Sports", "Movies"]},
        {"username": "user2", "name": "Jane", "age": 28, "gender": "Female", "location": "New York", "interests": ["Reading", "Traveling", "Cooking"]},
        {"username": "user3", "name": "Alex", "age": 22, "gender": "Male", "location": "Vancouver", "interests": ["Art", "Gaming", "Music"]},
        {"username": "user4", "name": "Sam", "age": 30, "gender": "Female", "location": "Toronto", "interests": ["Movies", "Cooking", "Art"]},
        {"username": "user5", "name": "Chris", "age": 27, "gender": "Male", "location": "New York", "interests": ["Sports", "Traveling", "Gaming"]},
        {"username": "user6", "name": "Taylor", "age": 24, "gender": "Female", "location": "Vancouver", "interests": ["Music", "Art", "Reading"]},
        {"username": "user7", "name": "Jordan", "age": 26, "gender": "Male", "location": "Toronto", "interests": ["Cooking", "Movies", "Sports"]},
        {"username": "user8", "name": "Morgan", "age": 29, "gender": "Female", "location": "New York", "interests": ["Traveling", "Music", "Gaming"]},
        {"username": "user9", "name": "Casey", "age": 23, "gender": "Male", "location": "Vancouver", "interests": ["Art", "Reading", "Movies"]},
        {"username": "user10", "name": "Denise", "age": 21, "gender": "Female", "location": "Toronto", "interests": ["Gaming", "Sports", "Cooking"]},
    ]

    # Insert each user into the database using the existing add_user function
    for user in users:
        add_user(
            username=user["username"],
            password=password,
            name=user["name"],
            age=user["age"],
            gender=user["gender"],
            location=user["location"],
            interests=user["interests"],
            introduction=f"Hi, I am {user['name']}. I love {', '.join(user['interests'])}."
        )

    print(f"10 dummy users created successfully in the database.")

if __name__ == "__main__":
    clean_database()

    create_tables()

    create_dummy_users()


