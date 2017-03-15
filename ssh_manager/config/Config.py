from ssh_manager.Connection import Connection
from ssh_manager.config.Commands.AbtractCommand import AbstractCommand
from ssh_manager.config.Commands.EditCommand import EditCommand
from ssh_manager.config.Commands.SshCommand import SshCommand
from ssh_manager.config.Window import Window


class Config:
    _connections = []
    _window = None
    _commands = {}

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

    def add_command(self, name: str, command: AbstractCommand):
        self._commands[name] = command

    def get_ssh_command(self) -> SshCommand:
        return self._commands['ssh']

    def get_edit_command(self) -> EditCommand:
        return self._commands['edit']
