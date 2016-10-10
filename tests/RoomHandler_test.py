from unittest.mock import MagicMock, Mock

from hypothesis import given
from hypothesis.strategies import text

from chat.Message import Message
from chat.Room import Room
from chat.RoomManager import RoomManager
from chat.UserManager import UserManager
from chat.handlers.RoomHandler import RoomHandler
from tests.BaseHandlerTest import BaseHandlerTest
from tests.Fixtures import MessageFixture
from tests.utils import some


class TestRoomHandler(BaseHandlerTest):
    def setup(self):
        super().setup()
        self.room_manager = RoomManager()
        self.user_manager = UserManager()
        self.handler = RoomHandler(
            self.app,
            self.request,
            room_manager=self.room_manager,
            user_manager=self.user_manager,
        )

    def cleanup(self):
        self.room_manager = None
        self.user_manager = None
        super().cleanup()

    def test_should_register_to_room_in_params(self):
        # given
        self.setup()
        mock_user = self.user_manager.create_user('test_user', 'valid token')
        self.request.headers.get_list = MagicMock(return_value=['valid token'])
        self.user_manager.find_by_token = MagicMock(return_value=mock_user)
        # when
        self.handler.open('some_room')
        # then
        assert self.handler.room.name == 'some_room'
        assert self.handler.user is not None
        assert self.handler.user.username == 'test_user'
        self.request.headers.get_list.assert_called_with('Authorization')
        # cleanup
        self.cleanup()

    def test_should_disconnect_if_auth_fails(self):
        # given
        self.setup()
        self.handler.write_message = MagicMock()
        self.handler.close = MagicMock()
        self.request.headers.get_list = MagicMock(return_value=None)
        self.user_manager.find_by_token = MagicMock(return_value=None)
        # when
        self.handler.open('some_room')
        # then
        assert self.handler.room is None
        assert self.handler.user is None
        self.request.headers.get_list.assert_called_with('Authorization')
        self.handler.close.assert_called_with()
        self.handler.write_message.assert_called_with(' 401 : unauthorized')
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
        self.handler.room.send_message.assert_called_with(some(Message))
        # cleanup
        self.cleanup()

    def test_should_disconnect(self):
        # given
        self.setup()
        self.handler.write_message = MagicMock()
        self.handler.close = MagicMock()
        # when
        self.handler.disconnect('some message')
        # then
        self.handler.close.assert_called_with()
        self.handler.write_message.assert_called_with('some message')
        # cleanup
        self.cleanup()

    def test_should_disconnect_if_user_does_not_exist(self):
            # given
            self.setup()
            self.handler.write_message = MagicMock()
            self.handler.close = MagicMock()
            self.handler.user = None
            # when
            self.handler.register_to_room('fake room')
            # then
            self.handler.close.assert_called_with()
            self.handler.write_message.assert_called_with(' 401 : unauthorized invalid token')
            # cleanup
            self.cleanup()
