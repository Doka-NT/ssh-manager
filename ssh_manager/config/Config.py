from ssh_manager.Connection import Connection
from ssh_manager.config.Window import Window


class Config:
    _connections = []
    _window = None

    def add_connection(self, connection: Connection):
        self._connections.append(connection)

    def set_window(self, window: Window):
        self._window = window

    def get_connections(self):
        return self._connections

    def get_window(self) -> Window:
        return self._window

    def set_connections(self, connections):
        self._connections = connections
