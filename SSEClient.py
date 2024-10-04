import ProxyDB


class SSEClient:
    def __init__(self, proxy: ProxyDB, buffer_size, cameras):
        self.proxy = proxy
        self.bufferSize = buffer_size
        self.cameras = cameras

    def openStream(self):
        ...

    def closeStream(self):
        ...
