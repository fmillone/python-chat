class Room:
    def __init__(self, name):
        self.clients = []
        self.name = name

    def __contains__(self, item):
        return item in self.clients

    def send_message(self, message):
        # todo: convert message to json
        for client in self.clients:
            client.write_message(message)

    def register(self, client):
        self.clients.append(client)

    def unsubscribe(self, client):
        self.clients.remove(client)

