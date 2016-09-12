from tornado.websocket import WebSocketHandler

from chat.Message import Message


class RoomHandler(WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self.data_store = None
        self.room_manager = None
        self.room = None
        super().__init__(application, request, **kwargs)

    def initialize(self, database, room_manager):
        self.data_store = database
        self.room_manager = room_manager
        assert self.room_manager is not None

    def open(self, room_name):
        self.room = self.room_manager.register(self, room_name)

    def send_message(self, message):
        self.room.send_message(message)

    def on_close(self):
        self.room.send_message('<username> disconnected')
        self.room.unsubscribe(self)

    def check_origin(self, origin):
        return True

    def on_message(self, raw_message):
        message = Message.from_json(raw_message)
        self.data_store.store_message(message)
        self.send_message(message)
