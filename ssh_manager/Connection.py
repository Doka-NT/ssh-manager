class Connection:
    DEFAULT_PORT = 22
    label = ''
    host = ''
    port = 0
    args = []

    def __init__(self, label: str, host: str, port: int, args: list):
        self.label = label
        self.host = host
        self.port = port
        self.args = args
