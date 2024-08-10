# user.py
#Account, password: Use to log in
# name: nick name or true name
# user_id: unique identifer for we to see and for user to match others

class User:
    def __init__(self, user_id, account, password, name, age, gender, location, interests,
                 liked_users=None, disliked_users=None, matches=None):
        # this user_ id unique id
        self.user_id = user_id
        self.account = account
        self.password = password
        self.name = name # true name
        self.age = age
        self.gender = gender
        self.location = location
        self.interests = interests
        self.liked_users = liked_users if liked_users is not None else []
        self.disliked_users = disliked_users if disliked_users is not None else []
        self.matches = matches if matches is not None else []

   # when print itself
    def __repr__(self):
        #TODO: need to make it more readable
        return (f'User({self.user_id}, {self.account}, {self.name}, {self.age}, {self.gender}, {self.location}, {self.interests},' 
            f'{self.liked_users}, {self.disliked_users}, {self.matches})')


    def like(self, other_user):
        if other_user.user_id not in self.liked_users:
            self.liked_users.append(other_user.user_id)
        if self.user_id in other_user.liked_users and other_user.user_id not in self.matches:
            self.matches.append(other_user.user_id)
            other_user.matches.append(self.user_id)

    def dislike(self, other_user):
        if other_user.user_id not in self.disliked_users:
            self.disliked_users.append(other_user.user_id)