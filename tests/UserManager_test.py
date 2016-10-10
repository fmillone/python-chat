from unittest.mock import MagicMock, Mock

from hypothesis import given
from hypothesis.strategies import text

from chat.User import User
from chat.UserManager import UserManager


class TestUserManager():
    def setup(self):
        self.manager = UserManager()

    def cleanup(self):
        self.manager = None

    def test_should_have_a_list_of_users(self):
        # given
        self.setup()
        # when
        # then
        assert self.manager.users == {}
        # cleanup
        self.cleanup()

    def test_should_create_an_user(self):
        # given
        self.setup()
        # when
        self.manager.create_user('username', 'token')
        # then
        assert len(self.manager.users) == 1
        # cleanup
        self.cleanup()

    def test_should_find_a_user_by_username(self):
        # given
        self.setup()
        self.manager.create_user('username', 'token')
        # when
        user = self.manager.find('username')
        # then
        assert user.username == 'username'
        assert user.token == 'token'
        assert type(user) is User
        # cleanup
        self.cleanup()

    def test_should_return_none(self):
        # given
        self.setup()
        # when
        user = self.manager.find('2')
        # then
        assert user is None
        # cleanup
        self.cleanup()

    def test_should_find_a_user_by_token(self):
        # given
        self.setup()
        self.manager.create_user('username', 'valid token')
        # when
        user = self.manager.find_by_token('valid token')
        # then
        assert user.username == 'username'
        assert user.token == 'valid token'
        assert type(user) is User
        # cleanup
        self.cleanup()
