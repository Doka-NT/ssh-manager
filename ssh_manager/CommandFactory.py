from ssh_manager.config.Commands.AbtractCommand import AbstractCommand
from ssh_manager.config.Commands.EditCommand import EditCommand
from ssh_manager.config.Commands.SshCommand import SshCommand


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
