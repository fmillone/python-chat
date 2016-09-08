from tornado.websocket import WebSocketHandler

from chat.DataStore import DATASTORE


class WebSockethandler(WebSocketHandler):
    CONNECTED_CLIENTS = []

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.dataStore = DATASTORE

    def on_message(self, message):
        self.dataStore.store_message(message)
        self.broadcast(message)

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
