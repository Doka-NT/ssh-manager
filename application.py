import argparse
from abc import ABCMeta, abstractmethod
from os.path import expanduser, sep

from gui.window import ConnectionListWindow
from manager.config import Config, ConfigurationFile
from manager.manager import Manager
from manager.parser import JsonConfigParser


class AbstractApplication:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._config_file_path = self.get_config_file_path()
        self._config = self.get_config(self._config_file_path)
        self._manager = self.get_manager(self._config)

    @abstractmethod
    def run(self):
        pass

    @staticmethod
    def get_config_file_path() -> str:
        home = expanduser("~")
        return home + sep + '.sshManager.config.json'

    @staticmethod
    def get_manager(config: Config):
        connections = config.get_connections()
        manager = Manager(connections)

        return manager

    @staticmethod
    def get_config(file_path: str) -> Config:
        file = ConfigurationFile(file_path)
        parser = JsonConfigParser()
        config = parser.parse(file)

        return config

    @staticmethod
    def create_default_manager():
        config = AbstractApplication.get_config(AbstractApplication.get_config_file_path())
        manager = AbstractApplication.get_manager(config)

        return manager


class GtkApplication(AbstractApplication):
    def run(self):
        window = ConnectionListWindow(
            self._manager,
            self._config.get_window(),
            self._config.get_ssh_command(),
            self._config.get_edit_command()
        )
        window.show()


class ConsoleApplication(AbstractApplication):
    def run(self):
        parser = argparse.ArgumentParser(description='Helps you to store and use SSH connections list')
        parser.add_argument(
            '--connection',
            '-c',
            help="Connect to specific server connection by it number. "
                 "Run program without arguments to list all available connections"
        )
        parser.add_argument('--edit', '-e', help="Edit configuration", action="store_true")
        args = parser.parse_args()

        if args.connection:
            connection = self._manager.get_connection(int(args.connection))
            self._connect_to(connection)
        if args.edit:
            self._edit_configuration()
        else:
            self._list_connections()

    def _connect_to(self, connection):
        self._config.get_ssh_command().run(connection, connection.args)

    def _list_connections(self):
        connections = self._manager.get_connections()
        print("Available connections:")
        for connection in connections:
            print("[{}]\t{}".format(connections.index(connection), connection.label))

    def _edit_configuration(self):
        self._config.get_edit_command().run(self._config_file_path)
