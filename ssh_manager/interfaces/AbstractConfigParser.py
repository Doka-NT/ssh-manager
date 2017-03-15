from abc import abstractmethod, ABCMeta

from ssh_manager import ConfigurationFile


class AbstractConfigParser:
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(self, file: ConfigurationFile):
        pass
