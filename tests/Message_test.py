from datetime import datetime

from hypothesis import given
from hypothesis.strategies import text

from chat.Message import Message


class TestMessage:
    message = None

    @given(author=text(), room=text(), content=text())
    def test_should_create_message(self, author, room, content):
        # given
        # when
        self.message = Message(author, content, room)
        # then
        assert self.message.author == author
        assert self.message.content == content
        assert self.message.room == room
        assert self.message.date.day == datetime.now().day
        assert self.message.date.month == datetime.now().month
        assert self.message.date.year == datetime.now().year
