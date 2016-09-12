from chat.Room import Room
from chat.utils.errors import IllegalArgumentError, InvalidRoomError


class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, name):
        if name is not None:
            room = Room(name)
            self.rooms[name] = room
            return room
        else:
            raise IllegalArgumentError('None is not a valid room name')

    def find_room(self, room_name):
        return self.rooms[room_name] if room_name in self.rooms else None

    def send_message(self, room_name, message):
        room = self.find_room(room_name)
        if room is not None:
            room.send_message(message)
        else:
            raise InvalidRoomError('There is no room named {}.'.format(room_name))

    def register(self, client, room_name):
        room = self.find_room(room_name)
        if room is None:
            room = self.create_room(room_name)
        room.register(client)
        return room


instance = RoomManager()
