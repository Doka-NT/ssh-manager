from manager.config import Connection


class Manager:
    _connections = []

    def __init__(self, connections: [Connection]):
        self._connections = connections

    def get_connection(self, index: int) -> Connection:
        return self._connections[index]

    def get_connections(self):
        return self._connections
