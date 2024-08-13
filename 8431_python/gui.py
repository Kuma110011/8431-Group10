import time
import sys
from datetime import datetime
import calendar
import random
from tkinter import Tk, Toplevel, Label, Entry, Button, messagebox, StringVar, OptionMenu, Listbox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from user import User
import database

class TinderLinkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TinderLink")
        self.user = None
        self.skipped_users = []  # Track skipped users during the current session
        self.create_login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()

        Label(self.root, text="Login", font=('Arial', 24)).pack(pady=10)

        Label(self.root, text="Username").pack(pady=5)
        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        Label(self.root, text="Password").pack(pady=5)
        self.password_entry = Entry(self.root, show='*')
        self.password_entry.pack()

        Button(self.root, text="Login", command=self.login).pack(pady=20)
        Button(self.root, text="Sign Up", command=self.create_signup_screen).pack(pady=5)
        Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def create_signup_screen(self):
        self.clear_screen()

        Label(self.root, text="Sign Up", font=('Arial', 24)).pack(pady=10)

        Label(self.root, text="Username").pack(pady=5)
        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        Label(self.root, text="Password").pack(pady=5)
        self.password_entry = Entry(self.root, show='*')
        self.password_entry.pack()

        Label(self.root, text="Name").pack(pady=5)
        self.name_entry = Entry(self.root)
        self.name_entry.pack()

        self.dob_label = Label(self.root, text="Date of Birth (YYYY-MM-DD)")
        self.dob_label.pack(pady=5)
        self.dob_entry = Entry(self.root)
        self.dob_entry.pack()

        Label(self.root, text="Gender").pack(pady=5)
        self.gender_var = StringVar(self.root)
        self.gender_var.set("Select")  # Default value
        gender_options = ["Male", "Female", "Unknown"]
        gender_menu = OptionMenu(self.root, self.gender_var, *gender_options)
        gender_menu.pack(pady=5)

        Label(self.root, text="Location").pack(pady=5)
        self.location_entry = Entry(self.root)
        self.location_entry.pack()

        Label(self.root, text="Interests (comma-separated)").pack(pady=5)
        self.interests_entry = Entry(self.root)
        self.interests_entry.pack()

        Label(self.root, text="Introduction").pack(pady=5)
        self.introduction_entry = Entry(self.root)
        self.introduction_entry.pack()

        Button(self.root, text="Sign Up", command=self.sign_up).pack(pady=20)
        Button(self.root, text="Back to Login", command=self.create_login_screen).pack(pady=5)

    def create_user_menu(self): 
        self.clear_screen()

        Label(self.root, text=f"Welcome, {self.user.name}!", font=('Arial', 24)).pack(pady=20)
        Button(self.root, text="Start Swiping", command=self.start_swiping).pack(pady=10)
        Button(self.root, text="View Profile", command=self.view_profile).pack(pady=10)
        Button(self.root, text="View Matches", command=self.view_matches).pack(pady=10)
        Button(self.root, text="Log Out", command=self.create_login_screen).pack(pady=20)

    def login(self):
        account = self.username_entry.get()
        password = self.password_entry.get()

        user_data = database.get_user(account)
        if user_data and user_data[2] == password:
            self.user = User(*user_data[:-1])
            self.user.assign_attribute_weights(json.loads(user_data[-1]))

            messagebox.showinfo("Success", f"Welcome, {self.user.name}!")
            self.create_user_menu()
        else:
            messagebox.showerror("Error", "Wrong Account or Password.")

    def sign_up(self):
        account = self.username_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()

        # Validate the date of birth
        try:
            dob = datetime.strptime(self.dob_entry.get(), "%Y-%m-%d")
        except ValueError:
            self.show_error_popup("The date of birth entered is out of range or invalid. Please enter a valid date.")
            return

        age = calculate_age(dob)
        gender = self.gender_var.get()
        location = self.location_entry.get()
        selected_interests = self.interests_entry.get().split(',')
        introduction = self.introduction_entry.get()

        if gender == "Select":
            messagebox.showerror("Error", "Please select a gender.")
            return

        existing_user = database.get_user(account)
        if existing_user:
            messagebox.showerror("Error", "Account already exists, please sign in.")
            return

        database.add_user(account, password, name, int(age), gender, location, selected_interests, introduction)
        messagebox.showinfo("Success", "You are registered. Please sign in.")
        self.create_login_screen()

    def show_error_popup(self, message):
        error_window = Toplevel(self.root)
        error_window.title("Error")

        Label(error_window, text=message, font=('Arial', 14)).pack(pady=10)
        Button(error_window, text="Back", command=error_window.destroy).pack(pady=10)

    def start_swiping(self):
        self.skipped_users = []

        all_users = [
            user for user in database.get_all_users()
            if user.user_id != self.user.user_id and
            user.user_id not in self.user.liked_users and
            user.user_id not in self.user.disliked_users
        ]

        if not all_users:
            self.no_more_users()
            return

        self.swipe_window = Toplevel(self.root)
        self.swipe_window.title("Start Swiping")

        self.swipe_index = 0
        self.all_users = all_users
        self.show_next_user()

    def show_next_user(self):
        if self.swipe_index >= len(self.all_users):
            self.swipe_window.destroy()
            self.no_more_users()
            return

        other_user_data = self.all_users[self.swipe_index]

        # Check if `other_user_data` is already a `User` object
        if isinstance(other_user_data, User):
            other_user = other_user_data
        else:
            other_user = User(*other_user_data)

        self.clear_swipe_window()

        Label(self.swipe_window, text="User Profile", font=('Arial', 24)).pack(pady=10)
        Label(self.swipe_window, text=f"Name: {other_user.name}").pack(pady=5)
        Label(self.swipe_window, text=f"Age: {other_user.age}").pack(pady=5)
        Label(self.swipe_window, text=f"Gender: {other_user.gender}").pack(pady=5)
        Label(self.swipe_window, text=f"Location: {other_user.location}").pack(pady=5)

        interests_display = ', '.join(other_user.interests) if isinstance(other_user.interests, list) else other_user.interests
        Label(self.swipe_window, text=f"Interests: {interests_display}").pack(pady=5)

        like_button = Button(self.swipe_window, text="Like", command=lambda u_id=other_user.user_id: self.like_user_and_continue(u_id))
        like_button.pack(side="left", padx=20, pady=10)

        dislike_button = Button(self.swipe_window, text="Dislike", command=lambda u_id=other_user.user_id: self.dislike_user_and_continue(u_id))
        dislike_button.pack(side="left", padx=20, pady=10)

        skip_button = Button(self.swipe_window, text="Skip", command=self.skip_user_and_continue)
        skip_button.pack(side="left", padx=20, pady=10)

        close_button = Button(self.swipe_window, text="X", command=self.close_swiping)
        close_button.place(relx=1.0, rely=0.0, anchor="ne")

    def close_swiping(self):
        self.swipe_window.destroy()
        self.create_user_menu()

    def like_user_and_continue(self, user_id):
        self.like_user(user_id)
        self.all_users.pop(self.swipe_index)
        self.show_next_user()

    def dislike_user_and_continue(self, user_id):
        self.dislike_user(user_id)
        self.all_users.pop(self.swipe_index)
        self.show_next_user()

    def skip_user_and_continue(self):
        self.skipped_users.append(self.all_users[self.swipe_index])
        self.swipe_index += 1
        self.show_next_user()

    def no_more_users(self):
        no_users_window = Toplevel(self.root)
        no_users_window.title("No More Users")

        Label(no_users_window, text="No more users to swipe.", font=('Arial', 24)).pack(pady=20)
        Button(no_users_window, text="Back to Menu", command=lambda: [no_users_window.destroy(), self.create_user_menu()]).pack(pady=20)

    def clear_swipe_window(self):
        for widget in self.swipe_window.winfo_children():
            widget.destroy()

    def view_profile(self):
        self.clear_screen()

        Label(self.root, text="Your Profile", font=('Arial', 24)).pack(pady=10)
        Label(self.root, text=f"Matching ID: {self.user.user_id}").pack(pady=5)
        Label(self.root, text=f"Account: {self.user.account}").pack(pady=5)
        Label(self.root, text=f"Name: {self.user.name}").pack(pady=5)
        Label(self.root, text=f"Age: {self.user.age}").pack(pady=5)
        Label(self.root, text=f"Gender: {self.user.gender}").pack(pady=5)
        Label(self.root, text=f"Location: {self.user.location}").pack(pady=5)

        interests_display = ', '.join(self.user.interests) if isinstance(self.user.interests, list) else self.user.interests
        Label(self.root, text=f"Interests: {interests_display}").pack(pady=5)
        Label(self.root, text=f"Introduction: {self.user.introduction}").pack(pady=5)

        Button(self.root, text="Edit Profile", command=self.edit_profile).pack(pady=10)
        Button(self.root, text="Delete Profile", command=self.delete_profile).pack(pady=10)
        Button(self.root, text="Back", command=self.create_user_menu).pack(pady=10)

    def edit_profile(self):
        self.clear_screen()

        Label(self.root, text="Edit Profile", font=('Arial', 24)).pack(pady=10)

        Label(self.root, text="Name").pack(pady=5)
        name_entry = Entry(self.root)
        name_entry.insert(0, self.user.name)
        name_entry.pack()

        Label(self.root, text="Age").pack(pady=5)
        age_entry = Entry(self.root)
        age_entry.insert(0, self.user.age)
        age_entry.pack()

        Label(self.root, text="Gender").pack(pady=5)
        gender_entry = Entry(self.root)
        gender_entry.insert(0, self.user.gender)
        gender_entry.pack()

        Label(self.root, text="Location").pack(pady=5)
        location_entry = Entry(self.root)
        location_entry.insert(0, self.user.location)
        location_entry.pack()

        Label(self.root, text="Interests (comma-separated)").pack(pady=5)
        interests_entry = Entry(self.root)
        interests_entry.insert(0, ', '.join(self.user.interests))
        interests_entry.pack()

        Label(self.root, text="Introduction").pack(pady=5)
        introduction_entry = Entry(self.root)
        introduction_entry.insert(0, self.user.introduction)
        introduction_entry.pack()

        def save_profile():
            self.user.name = name_entry.get()
            self.user.age = int(age_entry.get())
            self.user.gender = gender_entry.get()
            self.user.location = location_entry.get()
            self.user.interests = interests_entry.get().split(',')
            self.user.introduction = introduction_entry.get()
            database.update_user(self.user)
            messagebox.showinfo("Success", "Your profile has been updated.")
            self.create_user_menu()

        Button(self.root, text="Save", command=save_profile).pack(pady=20)
        Button(self.root, text="Cancel", command=self.view_profile).pack(pady=5)

    def delete_profile(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete your profile?")
        if confirm:
        # Fetch all users from the database
            all_users = database.get_all_users()

        # Iterate through each user to remove the deleted user's ID from their lists
        for user_data in all_users:
            if isinstance(user_data, User):
                other_user = user_data
            else:
                # Only unpack the first 12 fields
                other_user = User(*user_data[:12])

            # Remove this user's ID from the other user's liked, disliked, and matches lists
            if self.user.user_id in other_user.liked_users:
                other_user.liked_users.remove(self.user.user_id)
            if self.user.user_id in other_user.disliked_users:
                other_user.disliked_users.remove(self.user.user_id)
            if self.user.user_id in other_user.matches:
                other_user.matches.remove(self.user.user_id)

            # Update the other user's data in the database
            database.update_user(other_user)

        # Finally, delete the user from the database
        database.delete_user(self.user.user_id)

        # Inform the user that their profile has been deleted
        messagebox.showinfo("Deleted", "Your profile has been deleted.")

        # Go back to the very original login screen
        self.create_login_screen()



    def view_matches(self):
        self.clear_screen()

        # Ensure self.user.matches is a list of integers
        if isinstance(self.user.matches, str):
            self.user.matches = [int(uid) for uid in self.user.matches.split(',') if uid.isdigit()]

        matches = []
        for liked_user_id in self.user.liked_users:
            other_user_data = database.get_user_by_id(liked_user_id)

            # Check if the returned data is already a User object
            if isinstance(other_user_data, User):
                other_user = other_user_data  # Use it directly
            elif isinstance(other_user_data, (tuple, list)):
                other_user = User(*other_user_data)  # Unpack and create User object
            else:
                # Log an error or handle unexpected data types
                print(f"Unexpected data type for user: {type(other_user_data)}")
                continue

            if self.user.user_id in other_user.liked_users:
                matches.append(other_user)

                # Ensure mutual match is updated
                if self.user.user_id not in other_user.matches:
                    other_user.matches.append(self.user.user_id)
                    other_user.matches = ','.join(map(str, other_user.matches))
                    database.update_user(other_user)

                if other_user.user_id not in self.user.matches:
                    self.user.matches.append(other_user.user_id)
                    self.user.matches = ','.join(map(str, self.user.matches))
                    database.update_user(self.user)

        Label(self.root, text="Your Matches", font=('Arial', 24)).pack(pady=10)

        if matches:
            for match in matches:
                try:
                    match_button = Button(self.root, text=f"{match.name}, {match.age} years old, {match.location}",
                                          command=lambda m=match: self.show_match_profile(m))
                    match_button.pack(pady=5)
                except Exception as e:
                    print(f"Error displaying match: {e}")
                    messagebox.showerror("Error", f"Failed to display match profile: {e}")
        else:
            Label(self.root, text="No matches yet.").pack(pady=10)

        Button(self.root, text="Back", command=self.create_user_menu).pack(pady=20)

    def show_match_profile(self, match):
        self.clear_screen()

        Label(self.root, text="User Profile", font=('Arial', 24)).pack(pady=10)
        Label(self.root, text=f"Name: {match.name}").pack(pady=5)
        Label(self.root, text=f"Age: {match.age}").pack(pady=5)
        Label(self.root, text=f"Gender: {match.gender}").pack(pady=5)
        Label(self.root, text=f"Location: {match.location}").pack(pady=5)

        interests_display = ', '.join(match.interests) if isinstance(match.interests, list) else match.interests
        Label(self.root, text=f"Interests: {interests_display}").pack(pady=5)
        Label(self.root, text=f"Introduction: {match.introduction}").pack(pady=5)

        Button(self.root, text="Back", command=self.view_matches).pack(pady=20)

    def like_user(self, other_user_id):
        if isinstance(self.user.liked_users, str):
            self.user.liked_users = [int(uid) for uid in self.user.liked_users.split(',') if uid.isdigit()]

        if isinstance(self.user.matches, str):
            self.user.matches = [int(uid) for uid in self.user.matches.split(',') if uid.isdigit()]

        if other_user_id not in self.user.liked_users:
            self.user.liked_users.append(other_user_id)
            self.user.liked_users = ','.join(map(str, self.user.liked_users))
            database.update_user(self.user)

            liked_user_data = database.get_user_by_id(other_user_id)

            # Check if `liked_user_data` is already a `User` object
            if isinstance(liked_user_data, User):
                liked_user = liked_user_data
            else:
                liked_user = User(*liked_user_data)

            if isinstance(liked_user.liked_users, str):
                liked_user.liked_users = [int(uid) for uid in liked_user.liked_users.split(',') if uid.isdigit()]

            if self.user.user_id in liked_user.liked_users:
                if other_user_id not in self.user.matches:
                    self.user.matches.append(other_user_id)
                    self.user.matches = ','.join(map(str, self.user.matches))
                    database.update_user(self.user)

                if self.user.user_id not in liked_user.matches:
                    liked_user.matches.append(self.user.user_id)
                    liked_user.matches = ','.join(map(str, liked_user.matches))
                    database.update_user(liked_user)

    def dislike_user(self, other_user_id):
        if isinstance(self.user.disliked_users, str):
            self.user.disliked_users = [int(uid) for uid in self.user.disliked_users.split(',') if uid.isdigit()]

        if other_user_id not in self.user.disliked_users:
            self.user.disliked_users.append(other_user_id)
            self.user.disliked_users = ','.join(map(str, self.user.disliked_users))
            database.update_user(self.user)

def calculate_age(dob):
    today = datetime.today()
    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age


if __name__ == "__main__":
    database.create_tables()
    root = Tk()
    app = TinderLinkApp(root)
    root.mainloop()
