from chat.User import User


class UserManager:
    def __init__(self):
        self.users = {}

    def create_user(self, username, token):
        user = User()
        user.username = username
        user.token = token
        self.users[username] = user
        return user

    def find(self, username):
        return self.users.get(username, None)

    def find_by_token(self, token):
        found = None
        for user in self.users.values():
            if user.token == token:
                found = user
                break
        return found
