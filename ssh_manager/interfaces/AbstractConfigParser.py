from abc import abstractmethod, ABCMeta

from ssh_manager import ConfigurationFile
from ssh_manager.CommandFactory import CommandFactory


class AbstractConfigParser:
    __metaclass__ = ABCMeta
    _command_factory = None

    def __init__(self):
        self._command_factory = CommandFactory()

    @abstractmethod
    def parse(self, file: ConfigurationFile):
        pass
