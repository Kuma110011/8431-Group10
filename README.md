# Romantic Matching App


Rotmantic is a dating application facing Rotman students. This project allows users to create accounts, swiping to find other interesting user, interact with other users (e.g., like, dislike), and view matches. It also allows users to edit and delete their account profile. The application includes both a command-line interface (CLI) and a graphical user interface (GUI) for user interaction. The project is structured with four main Python files:
+ user.py
+ database.py
+ main.py
+ gui.py

## Table of Content
1. About the Project
2. Project Structure
3. Usage
4. Acknowledgements

## Project Structure

1. `user.py` file defines the `User` class, which employs Object-Oriented Programming principles to manage the attributes for each user in the system. Key features including:
+ Attributes:
    + `user_id (str)`: Unique identifier for each user.
    + `account (str)`: The username associated with the user’s account.
    + `password (str)`: The user's password.
    + `name (str)`: The user's real name.
    + `age (int)`: The user's age.
    + `gender (str)`: The user's gender.
    + `location (str)`: The user's location.
    + `interests (list)`: A list of the user’s interests, stored as strings.
    + `introduction (str)`: the bio for the user.
    + `liked_users`: A list of user IDs that the user has liked.
    + `disliked_users`: A list of user IDs that the user has disliked.
    + `matches`: A list of user IDs that have mutually liked each other (i.e., matches).

+ Methods: 
    + `like`: Allows a user to like another user. If there is a mutual like, a match is created.
    + `dislike`: Allows a user to dislike another user.

2. `database.py`


3. `main.py` defines our command line interface, it creates welcome menu, user menu, allows user to swipe, edit and delete its profile, and view matches. The main functions and their roles are as follows:

+ `welcome()`: Displays the welcome message and the main menu options: Sign In, Sign Up, and Exit.
+ `sign_up()`: a function that asks user to input the basic information(account, password, name, age, gender, location, interest, introduction) to create a new profile and ensures the user is not an existing user. After registration, the program prompts the current user to sign in.
+ `sign_in()`: Ask users to enter their account and password, if validate, returns a User object for the current user.
+ `main()`: The main loop of the program that displays the user menu and navigate between sign-up, sign-in, and exit options.
+ `user_menu()`: When signing in successfully, the function user_menu will be called to print out 4 options "Start swiping", "Your Own Profiles", "View matches", and "Log out" for the user to choose. 
    +  If the user chooses "Start swiping", `start_swiping(current_user)` will be called. This function asks the user to choose "like, dislike, or skip" on the recommended user, and the `recommend(current_user, all_users)` function is called inside the `start_swiping(user)`. It selects one attribute by probability based on the weight of each attribute, picks up a list of users who have the same selected attribute as the current user, and randomly recommends a user from the list to the current user. If introduction is the selected attribute, the function `semantic_similarity(text1, text2)` willed be called to calculate the semantic similarity between two users' introductions. Similar introductions are matched based on the semantic similarity score. If the user likes the recommended user, the recommended user will be added into the liked_users list of the current user. Vice versa.
    + If the user chooses "Your Own Profiles",  `view_own_profile(user)` is called. This function prints the profile of the user and provides 3 options "Edit Profile", "Delete Profile", and "Go back" for the user. If the user chooses "Edit Profile", `edit_profile()` function is called to present the user current profile and modify the profile based on the user's input. 
    + If the user chooses "View matches", `view_matches(user)` is called. This function adds the mutual users to the match list and shows the matching result to the user


