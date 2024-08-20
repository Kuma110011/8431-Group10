# RSM8431

Table of Content
1. About the Project
2. Usage
3. Roadmap
4. Acknowledgements


1. About the Project

Rotmantic is a dating application facing Rotman students. In addition to basic functions such as login and registration, with a clear GUI, users can easily edit profiles, swipe through other users' profiles and browse matches. The dynamic matching algorithm helps Rotmantic make a better recommendation to the user after each swiping. 


2. Usage

main.py (welcome menu - user menu - swiping - profile - match)

Main is our first command line interface. It interacts with user input, switching between different menus.
welcome() function is firstly called to show the user registraion and login page.

If the user chooses to registrate, sign_up() function will be called to ask for user's basic information(account, password, name, age, gender, location, interest, introduction) to create a new profile.

If the user chooses to login, sign_in() function will be called to ask for user's account and password.

When signing in successfully, the function user_menu will be called to print out 4 options "Start swiping", "Your Own Profiles", "View matches", and "Log out" for the user to choose. 

If the user chooses "Start swiping", start_swiping(current_user) will be called. This function asks the user to choose "like, dislike, or skip" on the recommended user, and the recommend(current_user, all_users) function is called inside the start_swiping(user). It selects one attribute by probability based on the weight of each attribute, picks up a list of users who have the same selected attribute as the current user, and randomly recommends a user from the list to the current user. If introduction is the selected attribute, the function semantic_similarity(text1, text2) willed be called to calculate the semantic similarity between two users' introductions. Similar introductions are matched based on the semantic similarity score. If the user likes the recommended user, the like(self, other_user,chosen_attr) method in the User Class will be called. The recommended user will be added into the liked_users list of the current user. Vice versa.

If the user chooses "Your Own Profiles", view_own_profile(user) is called. This function prints the profile of the user and provides 3 options "Edit Profile", "Delete Profile", and "Go back" for the user. If the user chooses "Edit Profile", edit_profile() function is called to present the user current profile and modify the profile based on the user's input. 

If the user chooses "View matches", view_matches(user) is called. This function adds the mutual users to the match list and shows the matching result to the user


