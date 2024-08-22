class User:
    """
    The User class storing and managing user-specific information (e.g., account details, 
    personal information such as gender, age, etc.) and allows for functionality including
    like/dislike, tracking mutual matches. This class also provide methods to adjust for 
    attribute weights that is central to the matching algorithm.
    
    === Attributes ===
    user_id: the unique identifier for the user, which is automatically assigned to the user.
    account: the username for sign in purpose.
    password: the password that associated with the account.
    name: the real name for the user.
    age: the age for the user.
    gender: the gender for the user.
    location: the location for the user.
    interest: a list of interests for the user.
    introduction: the bio for the user.
    liked_users: a list of user ids that are liked by the user.
    disliked_users: a list of user ids that are disliked by the user.
    matches: a list of user ids that are matched by the users. Only mutually liked users will be included.
    
    === Private Attributes ===
    _attribute_weights: a dictionary that mapping each attribute (age, gender Male, gender Female, location
    and each of the interests) to a weight.
    """
    user_id: int
    account: str
    password: str
    name: str
    gender: str
    location: str
    interests: list
    introduction: str
    liked_users: list[int]
    disliked_users: list[int]
    matches: list[int]
    _attribute_weights: dict
    
    
    def __init__(self, user_id, account, password, name, age, gender, location, interests,introduction,
                 liked_users=None, disliked_users=None, matches=None):
        self.user_id = user_id
        self.account = account
        self.password = password
        self.name = name  # true name
        self.age = age
        self.gender = gender
        self.location = location
        self.introduction = introduction
        
        # Convert string to list of correct data type
        self.interests = self._convert_to_list(interests, str)
        
        # Create liked_users, disliked_users, and matches list
        self.liked_users = self._convert_to_list(liked_users, int)
        self.disliked_users = self._convert_to_list(disliked_users, int)
        self.matches = self._convert_to_list(matches, int)

        # Initialize attribute_weights with default values
        self._attribute_weights = {
            'age': 1.0,
            'gender_Male': 1.0,
            'gender_Female': 1.0,
            'location': 1.0,
            'introduction': 1.0}

        for interest in self.interests:
            self._attribute_weights[interest] = 1.0

    def _convert_to_list(self, attr, data_type):
        """Helper method to convert a comma-separated string to a list of integers"""
        if isinstance(attr, str):
            return [data_type(item) for item in attr.split(',') if item.strip()] if attr else []
        return attr if attr is not None else []

    def update_weight(self, multiplier, chosen_attr):
        """Adjusts the weight of the chosen attribute for the current user, base on the
        multiplier."""
        if chosen_attr != None:
            self._attribute_weights[chosen_attr] *= multiplier
    
    def get_attribute_weights(self):
        """return the attribute weights"""
        return self._attribute_weights
    
    def assign_attribute_weights(self, dict):
        """assign attribute weights given <dict>"""
        self._attribute_weights = dict

    def like(self, other_user,chosen_attr):
        """like the other user if not already existed in the liked user list, and increase
        the weight by 1.1 for the matching attribute. If the user and the other user are
        mutually like, add the other user to the match list for the current user."""
        if other_user.user_id not in self.liked_users:
            self.liked_users.append(other_user.user_id)
        self.update_weight(1.1,chosen_attr)# increase weight for matched attributes 
        if self.user_id in other_user.liked_users and other_user.user_id not in self.matches:
            self.matches.append(other_user.user_id)
            other_user.matches.append(self.user_id)

    def dislike(self, other_user,chosen_attr):
        """Dislike the other user if not already existed in the disliked user list, and decrease
        the weight by 0.9 for the matching attribute. """
        if other_user.user_id not in self.disliked_users:
            self.disliked_users.append(other_user.user_id)
        self.update_weight(0.9, chosen_attr)  # decrease weight for unmatched attributes

    def __repr__(self):
        return (f'User({self.user_id}, {self.account}, {self.name}, {self.age}, {self.gender}, '
                f'{self.location}, {self.interests}, {self.liked_users}, {self.disliked_users}, {self.matches})')
