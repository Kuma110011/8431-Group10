# main.py
#test
#test2
import time
import sys
from user import User
import database
#123
def welcome():
    print("welcome to tinderlink!")
    print("1.Sign In")
    print("2.Sign Up")
    print("3.Exit")

def sign_up():
    print("Sign Up")
    account = input("Account: ")
    password = input("Password: ")
    name = input("UserName: ")
    #usr id is our id, also unique id
    age = int(input("Age: ")) ## need to check whether is digit
    gender = input("Gender: ")
    location = input("Location: ")
    interests = input("interests(Separated By Text): ").split(',')
    
    existing_user = database.get_user(account)
    if existing_user:
        print("Already exist, please sign in")
        return

    database.add_user(account, password, name, age, gender, location, interests)
    print("You are registered, this will be automatically close and please sign in")
    #sleep for 2 seconds to let user read the message
    time.sleep(2)

def sign_in():
    print("Sign In")
    account = input("Account: ")
    password = input("Password: ")
    
    user_data = database.get_user(account)
    if user_data and user_data[2] == password:  # user_data[2] is password
        print(f"Welcome, {user_data[3]}!")  # user_data[3] is name
        return User(*user_data)
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
                # Go to user menu
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


def start_swiping(user):
    all_users = database.get_users()# this thing needs alogrithm
    for other_user_data in all_users:
        other_user = User(*other_user_data)
        if other_user.user_id != user.user_id:
            print(other_user) 
            while True:
                action = input("Do you want to like (l), dislike (d), or exit (e)? ")
                if action == 'l':
                    # like_user(user, other_user.user_id)
                    user.like(other_user)
                    database.update_user(user)
                    break
                elif action == 'd':
                    # dislike_user(user, other_user.user_id)
                    user.dislike(other_user)
                    database.update_user(user)
                    break
                elif action == 'e':
                    return
                else:
                    print("Invalid choice, please try again.")
            
                    
                    
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
                database.delete_user(user.account) 
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
    user.age = int(input(f"Age ({user.age}): ") or user.age)
    user.gender = input(f"Gender ({user.gender}): ") or user.gender
    user.location = input(f"Location ({user.location}): ") or user.location
    if isinstance(user.interests, str):
        user.interests = input(f"Interests ({user.interests}): ").split(',') or user.interests
    else:
        user.interests = input(f"Interests ({', '.join(user.interests)}): ").split(',') or user.interests
    database.update_user(user) #update_user has not been created
    print("Your profile has been updated.")
#need to make sure cant like user itself

def like_user(user): # we dont need this function?
    user_id = int(input("Please enter the ID you like: "))
    user.like_user(user_id)
    print("User Liked.")

def dislike_user(user): # we dont need this function?
    user_id = int(input("Please enter the ID you dislike: "))
    user.dislike_user(user_id)
    print("User Disliked.")

#need to make sure cant like user itself
def view_matches(user):
    matches = []
    for liked_user_id in user.liked_users:
        other_user_data = database.get_user(liked_user_id)
        if other_user_data:
            other_user = User(*other_user_data)
            if user.user_id in other_user.liked_users:
                matches.append(other_user)
    
    print("Your matches:")
    for match in matches:
        print(match)

if __name__ == "__main__":
    main()
