import tornado.ioloop
import tornado.web

from chat.handlers.MainHandler import MainHandler
from chat.handlers.WebSockethandler import WebSockethandler


def make_app():
    return tornado.web.Application([
        (r"/home", MainHandler),
        (r"/", WebSockethandler),
    ])


if __name__ == "__main__":
    socket = make_app()
    socket.listen(9999)
    tornado.ioloop.IOLoop.current().start()
