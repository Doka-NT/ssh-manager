class Connection:
    DEFAULT_PORT = 22
    label = ''
    host = ''
    port = 0

    def __init__(self, label: str, host: str, port: int):
        self.label = label
        self.host = host
        self.port = port
