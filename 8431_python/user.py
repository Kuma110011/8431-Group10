# user.py
#Account, password: Use to log in
# name: nick name or true name
# user_id: unique identifer for we to see and for user to match others
class User:
    def __init__(self, user_id, account, password, name, age, gender, location, interests):
        # this user_ id unique id
        self.user_id = user_id
        self.account = account
        self.password = password
        self.name = name # true name
        self.age = age
        self.gender = gender
        self.location = location
        self.interests = interests
        self.liked_users = []
        self.disliked_users = []
        self.matches = []
   # when print itself
    def __repr__(self):
        return f"User({self.user_id}, {self.account}, {self.name}, {self.age}, {self.gender}, {self.location}, {self.interests})"

    def like_user(self, user_id):
        if user_id not in self.liked_users:
            self.liked_users.append(user_id)

    def dislike_user(self, user_id):
        if user_id not in self.disliked_users:
            self.disliked_users.append(user_id)
