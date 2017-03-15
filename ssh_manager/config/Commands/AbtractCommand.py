class AbstractCommand:
    _args = []

    def __init__(self, args: list):
        self._args = args

    def run(self, *args):
        pass
