from abc import ABCMeta, abstractmethod
from os.path import expanduser, sep

from gui.window import ConnectionListWindow
from manager.config import Config, ConfigurationFile
from manager.manager import Manager
from manager.parser import JsonConfigParser


class AbstractApplication:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        pass


class Application(AbstractApplication):
    def run(self):
        config_file_path = self.get_config_file_path()
        config = self.get_config(config_file_path)
        manager = self.get_manager(config)

        window = ConnectionListWindow(manager, config.get_window(), config.get_ssh_command(), config.get_edit_command())
        window.show()

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
        config = Application.get_config(Application.get_config_file_path())
        manager = Application.get_manager(config)

        return manager
