class User:
    def __init__(self, id, username, email, first_name=None, last_name=None):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        
    def __repr__(self):
        return f'<User {self.username}>'
        
    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        return self.username 