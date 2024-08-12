# user.py
#Account, password: Use to log in
# name: nick name or true name
# user_id: unique identifer for we to see and for user to match others

class User:
    def __init__(self, user_id, account, password, name, age, gender, location, interests,
                 liked_users=None, disliked_users=None, matches=None, attribute_weights=None):
        # this user_ id unique id
        self.user_id = user_id
        self.account = account
        self.password = password
        self.name = name # true name
        self.age = age
        self.gender = gender
        self.location = location
        
        # Convert string to list of correct data type if needed
        self.interests = self._convert_to_list(interests, str)
        
        # Create liked_users, disliked_users, and matches list
        self.liked_users = self._convert_to_list(liked_users, int)
        self.disliked_users = self._convert_to_list(disliked_users, int)
        self.matches = self._convert_to_list(matches, int)

        # Initialize attribute weights
        self.attribute_weights = {
            'age': 1.0,
            'gender': 1.0,
            'location': 1.0
        }
        for interest in self.interests:
            self.attribute_weights[interest] = 1.0


    def _convert_to_list(self, attr, data_type):
        # Filter out any empty strings before converting to the desired data type
        return list(map(data_type, filter(None, attr.split(',')))) if attr else []


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
        self.update_weight(other_user, 1.1)

    def dislike(self, other_user):
        if other_user.user_id not in self.disliked_users:
            self.disliked_users.append(other_user.user_id)

        self.update_weight(other_user, 0.9)


    def update_weight(self, other_user, factor):
        """Update the weight of the matched attribute."""
        for attr, weight in self.attribute_weights.items():
            if attr in ['age', 'gender', 'location']:
                if getattr(self, attr) == getattr(other_user, attr):
                    self.attribute_weights[attr] *= factor
            elif attr in self.interests and attr in other_user.interests:
                self.attribute_weights[attr] *= factor