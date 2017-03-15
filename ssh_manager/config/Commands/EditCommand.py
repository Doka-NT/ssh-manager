from os import system

from ssh_manager.config.Commands.AbtractCommand import AbstractCommand


class EditCommand(AbstractCommand):
    def run(self, *args):
        super().run(*args)
        cmd = self._args
        file = args[0]
        command = " ".join(cmd).replace("$file", file)
        system(command)
