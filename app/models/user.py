class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
        
    def __repr__(self):
        return f'<User {self.username}>' 