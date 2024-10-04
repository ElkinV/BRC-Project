from IDBConnection import IDBConnection


class SQLServerConnection(IDBConnection):
    def __init__(self, user: str, password: str, port: str, server: str, database: str):
        self.user = user
        self.password = password
        self.port = port
        self.server = server
        self.database = database

    def connect(self):
        pass

    def disconnect(self):
        pass

    def executeQuery(self):
        pass

    def checkConnection(self):
        pass

    def getCameras(self):
        pass