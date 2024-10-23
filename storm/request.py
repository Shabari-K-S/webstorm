class HTTPRequest:
    def __init__(self, data: bytes):
        self.method = None
        self.uri = None
        self.http_version = None
        self.parse(data)

    def parse(self, data: bytes):
        lines = data.split(b'\r\n')
        request_line = lines[0]
        words = request_line.split(b' ')
        self.method = words[0].decode()
        if len(words) > 1:
            self.uri = words[1].decode()
        if len(words) > 2:
            self.http_version = words[2].decode()
