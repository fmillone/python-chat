import tornado.web
from tornado.ioloop import IOLoop

from chat import DataStore
from chat.RoomManager import RoomManager
from chat.UserManager import UserManager
from chat.handlers.MainHandler import MainHandler
from chat.handlers.RoomHandler import RoomHandler
from chat.handlers.WebSockethandler import WebSockethandler

if __name__ == "__main__":
    handler_args = {'database': DataStore.instance, 'room_manager': RoomManager()}
    tornado.web.Application([
        (r'/home', MainHandler),
        # (r'/', WebSockethandler, handler_args),
        (r'/room/\w+(.*)\w+$', RoomHandler, {'room_manager': RoomManager(), 'user_manager': UserManager()}),
    ]).listen(9999)
    IOLoop.current().start()
