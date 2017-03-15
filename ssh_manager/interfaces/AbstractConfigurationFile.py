from abc import ABCMeta, abstractmethod


class AbstractConfigurationFile:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def get_contents(self):
        pass
