from unittest.mock import MagicMock, Mock

from hypothesis import given
from hypothesis.strategies import text

from chat.Message import Message
from chat.RoomManager import RoomManager
from chat.handlers.WebSockethandler import WebSockethandler
from tests.BaseHandlerTest import BaseHandlerTest
from tests.Fixtures import MessageFixture
from tests.utils import some


class TestWebSockethandler(BaseHandlerTest):
    def setup(self):
        super().setup()
        self.data_store = Mock()
        self.data_store.store_message = MagicMock()
        self.room_manager = RoomManager()
        self.handler = WebSockethandler(
            self.app,
            self.request,
            database=self.data_store,
            room_manager=self.room_manager
        )

    def cleanup(self):
        self.handler.CONNECTED_CLIENTS.clear()
        self.data_store = None
        self.room_manager = None
        super().cleanup()

    def test_should_store_message_and_broadcast(self):
        # given
        self.setup()
        message = MessageFixture.json_message()
        self.room_manager.create_room('a room')
        # when
        self.handler.on_message(message)
        # then
        self.data_store.store_message.assert_called_with(some(Message))
        # cleanup
        self.cleanup()

    def test_should_add_client(self):
        # given
        self.setup()
        # when
        self.handler.open()
        # then
        assert len(self.handler.CONNECTED_CLIENTS) == 1
        assert self.handler.CONNECTED_CLIENTS[0] is self.handler
        # cleanup
        self.cleanup()

    def test_should_check_origin(self):
        # given
        self.setup()
        origin = Mock()
        # when
        expected_result = self.handler.check_origin(origin)
        # then
        assert expected_result is True

    @given(text())
    def test_should_broadcast_to_all_clients(self, message):
        # given
        self.setup()
        self.handler.CONNECTED_CLIENTS.append(Mock())
        self.handler.CONNECTED_CLIENTS.append(Mock())
        # when
        self.handler.broadcast(message, all_but=None)
        assert len(self.handler.CONNECTED_CLIENTS) == 2
        # then
        for client in self.handler.CONNECTED_CLIENTS:
            client.write_message.assert_called_with(message)
        # cleanup
        self.cleanup()

    def test_should_broadcast_on_disconnect(self):
        # given
        self.setup()
        self.handler.write_message = MagicMock()
        self.handler.CONNECTED_CLIENTS.append(self.handler)
        self.handler.CONNECTED_CLIENTS.append(Mock())
        assert self.handler in self.handler.CONNECTED_CLIENTS

        # when
        self.handler.on_close()
        # then
        assert self.handler not in self.handler.CONNECTED_CLIENTS
        for client in self.handler.CONNECTED_CLIENTS:
            client.write_message.assert_called_with('disconnected')
        # cleanup
        self.cleanup()

    @given(text())
    def test_should_broadcast_to_all_clients_in_room(self, message):
        # given
        self.setup()
        mock_client = Mock()
        mock_client.write_message = MagicMock()
        mock_room = self.room_manager.create_room('test_room')
        mock_room.register(mock_client)
        # when
        self.handler.send_to_room('test_room', message)
        # then
        mock_client.write_message.assert_called_with(message)
        # cleanup
        self.cleanup()

    @given(text())
    def test_should_respond_an_error_if_there_is_no_room_with_that_name(self, message):
        # given
        self.setup()
        self.handler.write_message = MagicMock()
        # when
        self.handler.send_to_room('test_room', message)
        # then
        self.handler.write_message.assert_called_with('There is no room named test_room.')

        # cleanup
        self.cleanup()
