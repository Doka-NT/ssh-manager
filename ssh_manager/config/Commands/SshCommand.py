from os import system

from ssh_manager.Connection import Connection
from ssh_manager.config.Commands.AbtractCommand import AbstractCommand


class SshCommand(AbstractCommand):
    def run(self, *args):
        super().run(*args)
        connection = args[0]  # type: Connection
        command_args = args[1]  # type: list
        cmd = self._args + command_args
        command = " ".join(cmd).replace("$host", connection.host).replace("$port", str(connection.port))
        system(command)
