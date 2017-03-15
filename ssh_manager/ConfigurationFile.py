from os.path import exists, dirname
from shutil import copy

from ssh_manager.interfaces.AbstractConfigurationFile import AbstractConfigurationFile


class ConfigurationFile(AbstractConfigurationFile):
    _file_path = ''

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
        dist_file = dirname(__file__) + '/../resources/config-dist.json'
        copy(dist_file, self._file_path)
