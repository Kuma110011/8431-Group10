# Romantic Matching App

This project allows users to create accounts, swiping to find other interesting user, interact with other users (e.g., like, dislike), and view matches. It also allows users to edit and delete their account profile. The application includes both a command-line interface (CLI) and a graphical user interface (GUI) for user interaction. The project is structured with four main Python files:
+ user.py
+ database.py
+ main.py
+ gui.py


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