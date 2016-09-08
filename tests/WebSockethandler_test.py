from unittest.mock import MagicMock, Mock

from chat.handlers.WebSockethandler import WebSockethandler
from hypothesis import given
from hypothesis.strategies import text

from chat.DataStore import DATASTORE

from tests.BaseHandlerTest import BaseHandlerTest


class TestWebSockethandler(BaseHandlerTest):

    def setup(self):
        super().setup()
        DATASTORE.store_message = MagicMock()
        self.handler = WebSockethandler(self.app, self.request)

    def cleanup(self):
        self.handler.CONNECTED_CLIENTS.clear()
        super().cleanup()


    @given(text())
    def test_should_store_message_and_broadcast(self, message):
        # given
        self.setup()
        # when
        self.handler.on_message(message)
        # then
        DATASTORE.store_message.assert_called_with(message)
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
        #cleanup
        self.cleanup()
