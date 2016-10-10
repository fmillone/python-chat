from tornado.websocket import WebSocketHandler

from chat.Message import Message


class RoomHandler(WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        self.room_manager = None
        self.room = None
        self.user = None
        self.user_manager = None
        super().__init__(application, request, **kwargs)

    def initialize(self, room_manager, user_manager):
        self.room_manager = room_manager
        self.user_manager = user_manager

    def open(self, room_name):
        auth_headers = self.request.headers.get_list('Authorization')
        if auth_headers:
            self.user = self.user_manager.find_by_token(auth_headers[0])
            self.register_to_room(room_name)
        else:
            self.disconnect(' 401 : unauthorized')

    def send_message(self, message):
        self.room.send_message(message)

    def disconnect(self, message):
        self.write_message(message)
        self.close()

    def on_close(self):
        if self.room is not None:
            self.room.send_message('<username> disconnected')
            self.room.unsubscribe(self)

    def check_origin(self, origin):
        return True

    def on_message(self, raw_message):
        message = Message.from_json(raw_message)
        self.send_message(message)

    def register_to_room(self, room_name):
        if self.user is not None:
            self.room = self.room_manager.register(self, room_name)
        else:
            self.disconnect(' 401 : unauthorized invalid token')
