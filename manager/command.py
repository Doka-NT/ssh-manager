from abc import ABCMeta, abstractmethod
from os import system


class AbstractCommand:
    __metaclass__ = ABCMeta

    def __init__(self, args: list):
        self._args = args

    @abstractmethod
    def run(self, *args):
        pass


class EditCommand(AbstractCommand):
    def run(self, *args):
        super().run(*args)
        cmd = self._args
        f = args[0]
        command = " ".join(cmd).replace("$file", f)
        system(command)


class SshCommand(AbstractCommand):
    def run(self, connection, command_args, *args, **kwargs):
        super().run(*args)
        cmd = self._args + command_args
        command = " ".join(cmd).replace("$host", connection.host).replace("$port", str(connection.port))
        system(command)


class CommandFactory:
    def create_command(self, name: str, args: list) -> AbstractCommand:
        command = None
        if name == 'ssh':
            command = self.create_ssh_command(args)
        elif name == 'edit':
            command = self.create_edit_command(args)
        return command

    @staticmethod
    def create_ssh_command(args: list) -> AbstractCommand:
        return SshCommand(args)

    @staticmethod
    def create_edit_command(args: list) -> AbstractCommand:
        return EditCommand(args)
