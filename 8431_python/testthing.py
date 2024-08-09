List = []
class User:
    def __init__(self, user_id, username, password, name, age, gender, location, interests):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.name = name
        self.age = age
        self.gender = gender
        self.location = location
        self.interests = interests
        self.liked_users = []
        self.disliked_users = []
        self.matches = []

        