from abc import ABCMeta, abstractmethod


class AbstractApplication:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self):
        pass
