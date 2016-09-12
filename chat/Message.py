import json
from datetime import datetime


class MessageEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.isoformat()


class Message:
    def __init__(self, author, content, room):
        self.author = author
        self.content = content
        self.room = room
        self.date = datetime.now()

    @classmethod
    def from_json(cls, json_message):
        decoded = json.loads(json_message)
        return cls(decoded['author'], decoded['content'], decoded['room'])

    def to_json(self):
        return json.dumps(self.__dict__, cls=MessageEncoder,
                          sort_keys=True)
