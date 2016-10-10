from datetime import datetime

from hypothesis import given
from hypothesis.strategies import text

from chat.Message import Message
from tests.Fixtures import MessageFixture


class TestMessage:
    def setup(self, author=None, room=None, content=None):
        self.message = Message(author, content, room)

    def cleanup(self):
        self.message = None

    @given(author=text(), room=text(), content=text())
    def test_should_create_message(self, author, room, content):
        # given
        self.setup()
        # when
        self.message = Message(author, content, room)
        # then
        assert self.message.author == author
        assert self.message.content == content
        assert self.message.room == room
        assert self.message.date.day == datetime.now().day
        assert self.message.date.month == datetime.now().month
        assert self.message.date.year == datetime.now().year
        # cleanup
        self.cleanup()

    @given(author=text(), room=text(), content=text())
    def test_should_create_from_json(self, author, room, content):
        # given
        self.setup()
        json_message = MessageFixture.json_message(author, room, content)
        # when
        self.message = Message.from_json(json_message)
        # then
        assert self.message.author == author
        assert self.message.content == content
        assert self.message.room == room
        assert self.message.date.day == datetime.now().day
        assert self.message.date.month == datetime.now().month
        assert self.message.date.year == datetime.now().year
        # cleanup
        self.cleanup()

    def test_should_convert_to_json(self):
        # TODO: find out why this test fails randomly
        # given
        self.setup('author', 'room', 'content')

        # when
        json_message = self.message.to_json()
        # then
        message = Message.from_json(json_message)
        assert message.author == self.message.author
        assert message.content == self.message.content
        assert message.room == self.message.room
        assert message.date == self.message.date
        # cleanup
        self.cleanup()
