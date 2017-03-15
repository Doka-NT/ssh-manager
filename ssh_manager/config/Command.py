from ssh_manager.config.Commands.AbtractCommand import AbstractCommand


class Command:
    _commands = {}

    def add_command(self, name: str, handler: AbstractCommand):
        self._commands[name] = handler

    def get_command(self, name: str) -> AbstractCommand:
        return self._commands[name]
