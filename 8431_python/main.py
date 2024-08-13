# main.py

import time
import sys
from user import User
import database
from datetime import datetime
import calendar
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def welcome():
    print("welcome to tinderlink!")
    print("1.Sign In")
    print("2.Sign Up")
    print("3.Exit")


def get_valid_int_input(prompt, min, max):
    while True:
        try:
            value = int(input(prompt))
            if min <= value <= max:
                return value
            else:
                print("Please enter a valid date.")
        except ValueError:
            print("Please enter a valid integer.")


def get_user_dob():
    today = datetime.today()
    year = get_valid_int_input("Your year of birth (e.g., 1990): ", 1000, today.year)
    month = get_valid_int_input("Your month of birth (e.g., 8 for August): ", 1, 12)

    days_in_month = calendar.monthrange(year, month)
    day = get_valid_int_input("Your day of birth (e.g., 10): ", 1, days_in_month[1])

    dob = datetime(year, month, day)
    return dob


def calculate_age(dob):
    today = datetime.today()
    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age


def sign_up():
    print("Sign Up")
    account = input("Account: ")
    password = input("Password: ")
    name = input("UserName: ")
    age = calculate_age(get_user_dob())
    gender = input("Gender: ")
    location = input("Location: ")
    
    print("Select your interests from the following options (separated by commas):")
    print("""
    Travel, Music, Gym, Tattoos, Coffee, Films, Walking, Netflix, Shopping, Outdoors,
    Football, Gym, Sports, Music, Films, Working Out, Tattoos, Outdoors, Nightlife
    """)
    interests = input("interests(Separated By Text): ").split(',')
    introduction = input("Introduction: ")
    existing_user = database.get_user(account)
    if existing_user:
        print("Already exist, please sign in")
        return
    
    database.add_user(account, password, name, age, gender, location, interests, introduction)
    
    print("You are registered, this will be automatically close and please sign in")
    time.sleep(2)

def sign_in():
    print("Sign In")
    account = input("Account: ")
    password = input("Password: ")
    
    user_data = database.get_user(account)
    if user_data and user_data[2] == password:
        print(f"Welcome, {user_data[3]}!")
        current_user = User(*user_data[:-1])
        current_user.assign_attribute_weights(json.loads(user_data[-1])
        return current_user
    else:
        print("Wrong Account or Password.")
        return None

def main():
    database.create_tables()

    while True:
        welcome()
        choice = input("Please choose an option: ")
        
        if choice == '1':
            user = sign_in()
            if user:
                user_menu(user)
        elif choice == '2':
            sign_up()
        elif choice == '3':
            sys.exit()
        else:
            print("Invalid choice, please try again.")

def user_menu(user):
    while True:
        print(f"\nWelcome {user.name}")
        print("1. Start swiping")
        print("2. Your Own Profiles")
        print("3. View matches")
        print("4. Log out")
        
        choice = input("Please select what to do: \n")
        
        if choice == '1':
            start_swiping(user)
        elif choice == '2':
            view_own_profile(user)
        elif choice == '3':
            view_matches(user)
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")

def recommend(current_user, all_users):
    excluded_users = set(current_user.liked_users + current_user.disliked_users)
    available_users = [user for user in all_users if user.user_id not in excluded_users and user.user_id != current_user.user_id]

    total_weight = sum(current_user.get_attribute_weights().values())
    chosen_attr = random.choices(
        population=list(current_user.get_attribute_weights().keys()),
        weights=list(current_user.get_attribute_weights().values()),
        k=1
    )[0]

    if chosen_attr == 'age':
        candidates = [user for user in available_users if abs(user.age - current_user.age) <= 5]
    elif chosen_attr == 'gender_Male':
        candidates = [user for user in available_users if user.gender.lower() == 'male']
    elif chosen_attr == 'gender_Female':
        candidates = [user for user in available_users if user.gender.lower() == 'female']
    elif chosen_attr == 'location':
        candidates = [user for user in available_users if user.location == current_user.location]
    elif chosen_attr == 'introduction':
        candidates = sorted(available_users, key=lambda user: semantic_similarity(current_user.introduction, user.introduction), reverse=True)
        candidates = candidates[:10]
    else:
        candidates = [user for user in available_users if chosen_attr in user.interests]

    if candidates:
        return random.choice(candidates)
    else:
        if available_users == []:
            print("No more users for recommendation")
            return None
        else:
            return random.choice(available_users)
        
def semantic_similarity(text1, text2):
    texts = [text1, text2]
    vectorizer = TfidfVectorizer().fit_transform(texts)
    similarity_matrix = cosine_similarity(vectorizer)
    return similarity_matrix[0, 1]

def start_swiping(current_user):
    all_users = database.get_all_users()
    all_users = [user for user in all_users if user.user_id != current_user.user_id] #list of User objects
   
    while True:

        recommended_user = recommend(current_user, all_users)

        print(f"\nRecommended User: {recommended_user}")
        if recommended_user is None:
            return
        
        action = input("Do you like this user? (yes/no/exit): ").lower()

        if action == "yes":
            current_user.like(recommended_user)
            database.update_user(current_user)
            all_users.remove(recommended_user)  # 从推荐列表中移除已处理的用户
        elif action == "no":
            current_user.dislike(recommended_user)
            database.update_user(current_user)
            all_users.remove(recommended_user)  # 从推荐列表中移除已处理的用户
        elif action == "exit":
            break
        else:
            print("Invalid input. Please enter 'yes', 'no', or 'exit'.")

        if not all_users:
            print('No more users to recommend.')
            break  
                    
                    
def view_own_profile(user):
    while True:
        print("\nYour Profile")
        print(f"Your Mathching ID: {user.user_id}")
        print(f"Account: {user.account}")
        print(f"Name: {user.name}")
        print(f"Age: {user.age}")
        print(f"Gender: {user.gender}")
        print(f"Location: {user.location}")
        
        if isinstance(user.interests, list):
            print(f"Interests: {', '.join(user.interests)}")
        else:
            print(f"Interests: {user.interests}")
        print(f"introduction: {user.introduction}")
        
        print(f"Liked users: {user.liked_users}")
        print(f"Disliked users: {user.disliked_users}")
        print(f"Matches: {user.matches}")

        print("\nOptions:")
        print("1. Edit Profile")
        print("2. Delete Profile")
        print("3. Go Back")

        choice = input("Choose an option: ")

        if choice == "1":
            edit_profile(user)
        elif choice == "2":
            confirm = input("Are you sure you want to delete your profile? (yes/no): ")
            if confirm.lower() == "yes":
                database.delete_user(user.user_id) 
                print("Your profile has been deleted.")
                sys.exit()  
            else:
                continue
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def edit_profile(user):
    print("\nEdit Profile")
    user.name = input(f"Name ({user.name}): ") or user.name
    user.gender = input(f"Gender ({user.gender}): ") or user.gender
    user.location = input(f"Location ({user.location}): ") or user.location
    if isinstance(user.interests, str):
        user.interests = input(f"Interests ({user.interests}): ").split(',') or user.interests
    else:
        user.interests = input(f"Interests ({', '.join(user.interests)}): ").split(',') or user.interests
    user.introduction = input(f"introduction ({user.introduction}): ") or user.introduction
    database.update_user(user)
    print("Your profile has been updated.")

def view_matches(user):
    matches = []
    for liked_user_id in user.liked_users:
        other_user = database.get_user_by_id(liked_user_id)
        if isinstance(other_user, User):
            if user.user_id in other_user.liked_users:
                matches.append(other_user)
    
    print("Your matches:")
    for match in matches:
        print(match)

if __name__ == "__main__":
    main()
