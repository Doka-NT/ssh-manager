from json import loads

from ssh_manager import ConfigurationFile
from ssh_manager.Connection import Connection
from ssh_manager.config.Config import Config
from ssh_manager.config.Window import Window
from ssh_manager.interfaces.AbstractConfigParser import AbstractConfigParser


class JsonConfigParser(AbstractConfigParser):
    def parse(self, file: ConfigurationFile) -> Config:
        config = Config()
        json_object = loads(file.get_contents())

        self._parse_connections(json_object, config)
        self._parse_window(json_object, config)
        self._parse_commands(json_object, config)

        return config

    @staticmethod
    def _parse_connections(json_object: dict, config: Config):
        config.set_connections([])
        for _connection in json_object['connections']:
            if 'port' not in _connection:
                _connection['port'] = Connection.DEFAULT_PORT
            if 'args' not in _connection:
                _connection['args'] = []
            connection = Connection(
                _connection['label'],
                _connection['host'],
                _connection['port'],
                _connection['args']
            )
            config.add_connection(connection)

    @staticmethod
    def _parse_window(json_object: dict, config: Config):
        _window = json_object['window']
        window = Window(_window['x'], _window['y'], _window['width'], _window['height'])
        config.set_window(window)

    def _parse_commands(self, json_object: dict, config: Config):
        for name, args in json_object['command'].items():
            command = self._command_factory.create_command(name, args)
            config.add_command(name, command)
