from unittest.mock import MagicMock, Mock

import pytest
from hypothesis import given
from hypothesis.strategies import text

from chat.Room import Room
from chat.RoomManager import RoomManager
from chat.utils.errors import IllegalArgumentError, InvalidRoomError


class TestRoomManager:
    def setup(self):
        self.manager = RoomManager()

    def cleanup(self):
        self.manager = None

    def test_should_have_a_dict_for_rooms(self):
        # given
        self.setup()
        # when
        # then
        assert self.manager.rooms == {}
        # cleanup
        self.cleanup()

    def test_should_add_a_room(self):
        # given
        self.setup()
        # when
        self.manager.create_room('roomName')
        # then
        assert len(self.manager.rooms) == 1
        assert type(self.manager.rooms['roomName']) == Room

        # cleanup
        self.cleanup()

    def test_should_not_add_a_room(self):
        # given
        self.setup()
        # when
        with pytest.raises(IllegalArgumentError) as error:
            self.manager.create_room(None)
        # then
        assert str(error.value) == 'None is not a valid room name'
        # cleanup
        self.cleanup()

    @given(text())
    def test_should_get_a_room_by_name(self, room_name):
        # given
        self.setup()
        self.manager.create_room(room_name)
        # when
        room = self.manager.find_room(room_name)
        # then
        assert room.name == room_name
        # cleanup
        self.cleanup()

    def test_should_not_get_a_room_by_none_name(self):
        # given
        self.setup()
        # when
        room = self.manager.find_room(None)
        # then
        assert room is None
        # cleanup
        self.cleanup()

    @given(text())
    def test_should_send_message_to_room(self, message):
        # given
        self.setup()
        test_room = self.manager.create_room('test_room')
        test_room.send_message = MagicMock()
        test_room2 = self.manager.create_room('test_room2')
        test_room2.send_message = MagicMock()

        # when
        self.manager.send_message('test_room', message)
        # then
        test_room.send_message.assert_called_with(message)
        test_room2.send_message.assert_not_called()
        # cleanup
        self.cleanup()

    @given(text(), text())
    def test_should_raise_an_error(self, room, message):
        # given
        self.setup()
        # when
        with pytest.raises(InvalidRoomError) as error:
            self.manager.send_message(room, message)
        # then
        assert str(error.value) == 'There is no room named {}.'.format(room)
        # cleanup
        self.cleanup()

    def test_should_register_to_room(self):
        # given
        self.setup()
        room = self.manager.create_room('test_room')
        client = Mock()
        # when
        self.manager.register(client, 'test_room')
        # then
        assert room.clients[0] is client
        # cleanup
        self.cleanup()

    def test_should_create_and_register_to_room(self):
        # given
        self.setup()
        client = Mock()
        # when
        self.manager.register(client, 'test_room')
        # then
        room = self.manager.find_room('test_room')
        assert room.clients[0] is client
        # cleanup
        self.cleanup()
