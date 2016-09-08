class _DataStore:
    def __init__(self):
        self.__messages = []

    def store_message(self, message):
        self.__messages.append(message)

    @property
    def messages(self):
        return self.__messages

    def clean(self):
        self.__messages = []


DATASTORE = _DataStore()
