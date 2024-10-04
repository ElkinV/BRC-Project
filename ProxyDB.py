import SQLServerConnection
from IDBConnection import IDBConnection


class ProxyDB(IDBConnection):
    def __init__(self, real_connection: SQLServerConnection, isConnected: bool = False):
        self.isConnected = isConnected
        self.real_connection = real_connection
        self.cache = {}  # Diccionario para almacenar las ip de las camaras en caché

    def connect(self):
        if not self.isConnected:
            self.real_connection.connect()
            self.isConnected = True
            print("Proxy conectado a la base de datos real")
        else:
            print("Ya está conectado")

    def disconnect(self):
        if self.isConnected:
            self.real_connection.disconnect()
            self.isConnected = False
            print("Proxy desconectado de la base de datos real")
        else:
            print("No hay conexión activa")

    def executeQuery(self, query: str)

        self.real_connection.executeQuery(query)

    def getCameras(self):
        # Método específico para obtener cámaras
        query = "SELECT camara_id, ip FROM API_camaras"
        if self.cache[query] in self.cache.:
            print("Devolviendo cámaras desde la caché")
            return self.cache[query]

        print("Obteniendo cámaras desde la base de datos real")
        cameras = self.real_connection.getCameras()
        self.cache[query] = cameras  # Guardar cámaras en la caché
        return cameras

    def clearCache(self):
        """Método para limpiar la caché."""
        self.cache.clear()
        print("Caché limpiada")
