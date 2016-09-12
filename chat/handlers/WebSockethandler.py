from tornado.websocket import WebSocketHandler

from chat.Message import Message
from chat.utils.errors import InvalidRoomError


class WebSockethandler(WebSocketHandler):
    CONNECTED_CLIENTS = []

    def __init__(self, application, request, **kwargs):
        self.data_store = None
        self.room_manager = None
        self.username = None
        super().__init__(application, request, **kwargs)

    def initialize(self, database, room_manager):
        self.data_store = database
        self.room_manager = room_manager

    def on_message(self, raw_message):
        msg = Message.from_json(raw_message)
        self.data_store.store_message(msg)

        self.send_to_room(msg.room, msg)

    def open(self):
        self.CONNECTED_CLIENTS.append(self)
        print('websocket opened')

    def check_origin(self, origin):
        return True

    @staticmethod
    def broadcast(pkg, all_but=None):
        for client in WebSockethandler.CONNECTED_CLIENTS:
            if client != all_but:
                client.write_message(pkg)

    def on_close(self):
        self.broadcast(self.create_leave_pkg(), all_but=self)
        print('websocket closed')
        self.CONNECTED_CLIENTS.remove(self)

    def create_leave_pkg(self):
        return 'disconnected'

    def send_to_room(self, room_name, message):
        try:
            self.room_manager.send_message(room_name, message)
        except InvalidRoomError as error:
            self.write_message(str(error))
