from IDBConnection import IDBConnection


class ProxyDB(IDBConnection):

    def __init__(self, real_connection: IDBConnection, isConnected: bool):
        self.isConnected = isConnected
        self.real_connection = real_connection

    def executeQuery(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass
