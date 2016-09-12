from unittest.mock import MagicMock, Mock

from hypothesis import given
from hypothesis.strategies import text

from chat.Message import Message
from chat.Room import Room
from chat.RoomManager import RoomManager
from chat.handlers.RoomHandler import RoomHandler
from tests.BaseHandlerTest import BaseHandlerTest
from tests.Fixtures import MessageFixture
from tests.utils import some


class TestRoomHandler(BaseHandlerTest):
    def setup(self):
        super().setup()
        self.data_store = MagicMock()
        self.room_manager = RoomManager()
        self.handler = RoomHandler(
            self.app,
            self.request,
            database=self.data_store,
            room_manager=self.room_manager
        )

    def cleanup(self):
        self.data_store = None
        self.room_manager = None
        super().cleanup()

    def test_should_register_to_room_in_params(self):
        # given
        self.setup()
        # when
        self.handler.open('some_room')
        # then
        assert self.handler.room.name == 'some_room'
        # cleanup
        self.cleanup()

    @given(text())
    def test_should_broadcast_to_all_clients_in_room(self, message):
        # given
        self.setup()
        self.handler.room = Room('test_room')
        self.handler.room.send_message = MagicMock()
        # when
        self.handler.send_message(message)
        # then
        self.handler.room.send_message.assert_called_with(message)
        # cleanup
        self.cleanup()

    def test_should_broadcast_on_disconnect(self):
        # given
        self.setup()
        # self.handler.room = Room('test_room')
        self.handler.room = MagicMock()
        # when
        self.handler.on_close()
        # then
        self.handler.room.send_message.assert_called_with('<username> disconnected')
        self.handler.room.unsubscribe.assert_called_with(self.handler)
        # cleanup
        self.cleanup()

    def test_should_check_origin(self):
        # given
        self.setup()
        origin = Mock()
        # when
        # then
        assert self.handler.check_origin(origin) is True
        # cleanup
        self.cleanup()

    def test_should_store_message_and_broadcast(self):
        # given
        self.setup()
        self.handler.room = MagicMock()
        message = MessageFixture.json_message()
        # when
        self.handler.on_message(message)
        # then
        self.data_store.store_message.assert_called_with(some(Message))
        self.handler.room.send_message.assert_called_with(some(Message))
        # cleanup
        self.cleanup()
