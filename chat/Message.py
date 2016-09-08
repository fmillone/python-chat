from datetime import datetime


class Message:
    def __init__(self, author, content, room):
        self.author = author
        self.content = content
        self.room = room
        self.date = datetime.now()
