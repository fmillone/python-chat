import json


class MessageFixture:
    @staticmethod
    def json_message(author='an author', room='a room', content='bla bla bla'):
        return json.dumps(MessageFixture.dict_message(author, room, content))

    @staticmethod
    def dict_message(author='an author', room='a room', content='bla bla bla'):
        return {'author': author, 'room': room, 'content': content}
