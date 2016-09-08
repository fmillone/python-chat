from hypothesis import given, example
from hypothesis.strategies import text

from chat.DataStore import _DataStore


class TestDataStore:
    dataStore = None

    def setup(self):
        self.dataStore = _DataStore()

    def cleanup(self):
        self.dataStore = None

    @given(text())
    @example('msg')
    def test_should_store_messages(self, message):
        # given
        self.setup()
        self.dataStore.store_message(message)
        self.dataStore.store_message(message * 2)
        # when
        actual_messages = self.dataStore.messages
        # then
        assert len(actual_messages) == 2
        assert actual_messages == [message, message * 2]
        # cleanup
        self.cleanup()

    @given(text())
    def test_should_return_empty_list(self, msg):
        # given
        self.setup()
        # when
        actual_message = self.dataStore.messages
        # then
        assert actual_message == []
        # cleanup
        self.cleanup()

    def test_should_clean_the_datastore(self):
        # given
        self.setup()
        self.dataStore.store_message('message')
        # when
        self.dataStore.clean()
        # then
        assert self.dataStore.messages == []
        # cleanup
        self.cleanup()
