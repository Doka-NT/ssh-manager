from abc import ABCMeta, abstractmethod
from genericpath import exists
from os.path import dirname, join
from shutil import copy

from manager.command import EditCommand, SshCommand, AbstractCommand


class Window:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        pass


class Command:
    _commands = {}

    def add_command(self, name: str, handler: AbstractCommand):
        self._commands[name] = handler

    def get_command(self, name: str) -> AbstractCommand:
        return self._commands[name]


class Connection:
    DEFAULT_PORT = 22

    def __init__(self, label: str, host: str, port: int, args: list):
        self.label = label
        self.host = host
        self.port = port
        self.args = args


class Config:
    def __init__(self) -> None:
        self._connections = []
        self._window = None
        self._commands = {}

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


class AbstractConfigurationFile:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_contents(self):
        pass


class ConfigurationFile(AbstractConfigurationFile):
    def __init__(self, file_path):
        super(ConfigurationFile, self).__init__()
        self._file_path = file_path
        self._create_if_not_exists()

    def get_contents(self):
        with open(self._file_path, 'r') as opened_file:
            return opened_file.read()

    def _create_if_not_exists(self):
        if exists(self._file_path):
            return
        dist_file = join(dirname(__file__), '..', 'resources', 'config-dist.json')
        copy(dist_file, self._file_path)
