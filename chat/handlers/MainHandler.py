from tornado.web import RequestHandler
from datetime import datetime


class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world at {}".format(datetime.now()))
