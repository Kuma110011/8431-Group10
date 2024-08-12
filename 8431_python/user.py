# user.py

class User:
    def __init__(self, user_id, account, password, name, age, gender, location, interests,introduction,
                 liked_users=None, disliked_users=None, matches=None,attribute_weights = None):
        self.user_id = user_id
        self.account = account
        self.password = password
        self.name = name  # true name
        self.age = age
        self.gender = gender
        self.location = location
        self.introduction = introduction
        
        # Convert string to list of correct data type if needed
        self.interests = self._convert_to_list(interests, str)
        
        # Create liked_users, disliked_users, and matches list
        self.liked_users = self._convert_to_list(liked_users, int)
        self.disliked_users = self._convert_to_list(disliked_users, int)
        self.matches = self._convert_to_list(matches, int)

        # Initialize attribute_weights with default values
        self.attribute_weights = {
            'age': 1.0,
            'gender_Male': 1.0,
            'gender_Female': 1.0,
            'location': 1.0,
            'introduction': 1.0,
            # You can add other attributes as needed
        }

    def _convert_to_list(self, attr, data_type):
        """Helper method to convert a comma-separated string to a list of integers"""
        if isinstance(attr, str):
            return [data_type(item) for item in attr.split(',') if item.strip()] if attr else []
        return attr if attr is not None else []

    def update_weight(self, other_user, multiplier):
        """Adjusts the weight of matching attributes between this user and another user."""
        for attr in self.attribute_weights:
            if hasattr(self, attr) and hasattr(other_user, attr):
                if getattr(self, attr) == getattr(other_user, attr):
                    self.attribute_weights[attr] *= multiplier

    def like(self, other_user):
        if other_user.user_id not in self.liked_users:
            self.liked_users.append(other_user.user_id)
        self.update_weight(other_user, 1.1)  # increase weight for matched attributes
        if self.user_id in other_user.liked_users and other_user.user_id not in self.matches:
            self.matches.append(other_user.user_id)
            other_user.matches.append(self.user_id)

    def dislike(self, other_user):
        if other_user.user_id not in self.disliked_users:
            self.disliked_users.append(other_user.user_id)
        self.update_weight(other_user, 0.9)  # decrease weight for unmatched attributes

    def __repr__(self):
        return (f'User({self.user_id}, {self.account}, {self.name}, {self.age}, {self.gender}, '
                f'{self.location}, {self.interests}, {self.liked_users}, {self.disliked_users}, {self.matches})')
