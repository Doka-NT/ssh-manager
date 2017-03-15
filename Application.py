from os.path import expanduser, sep

from ssh_manager.ConfigurationFile import ConfigurationFile
from ssh_manager.JsonConfigParser import JsonConfigParser
from ssh_manager.Manager import Manager
from ssh_manager.config.Config import Config
from ssh_manager.interfaces.AbstractApplication import AbstractApplication
from ui.ConnectionListWindow import ConnectionListWindow


class Application(AbstractApplication):
    def run(self):
        config_file_path = self.get_config_file_path()
        config = self.get_config(config_file_path)
        manager = self.get_manager(config)

        window = ConnectionListWindow(manager, config.get_window())
        window.show()

    @staticmethod
    def get_config_file_path() -> str:
        home = expanduser("~")
        return home + sep + '_______sshManager.config.json'

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
