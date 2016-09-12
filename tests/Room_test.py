from unittest.mock import Mock

from hypothesis import given
from hypothesis.strategies import text

from chat.Room import Room


class TestRoom:
    def setup(self, room_name='test room'):
        self.room = Room(room_name)

    def cleanup(self):
        self.room = None

    @given(text())
    def test_should_have_a_list_of_clients(self, room_name):
        # given
        self.setup(room_name)
        # when
        # then
        assert self.room.clients == []
        assert self.room.name == room_name
        # cleanup
        self.cleanup()

    @given(text())
    def test_should_broadcast_send_message_to_all_clients_in_room(self, message):
        # given
        self.setup()
        client_one = Mock()
        client_two = Mock()
        self.room.clients.append(client_one)
        self.room.clients.append(client_two)
        # when
        self.room.send_message(message)
        # then
        client_one.write_message.assert_called_with(message)
        # cleanup
        self.cleanup()

    def test_should_unsubscribe_a_client(self):
        # given
        self.setup()
        client_one = Mock()
        self.room.clients.append(client_one)
        # when
        self.room.unsubscribe(client_one)
        # then
        assert client_one not in self.room
        # cleanup
        self.cleanup()
