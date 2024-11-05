from SQLServerConnection import SQLServerConnection
from IDBConnection import IDBConnection
import logging

logger = logging.getLogger(__name__)

class ProxyDB(IDBConnection):
    def __init__(self, real_connection: SQLServerConnection, isConnected):
        self.real_connection = real_connection
        self.cache = {}  # Diccionario para almacenar las ip de las camaras en caché
        self.isConnected = real_connection.checkConnection()

    def connect(self):
        if not self.isConnected:
            self.real_connection.connect()
            self.isConnected = True
            logger.info("Proxy conectado a la base de datos real")
        else:
            logger.info("Ya está conectado")

    def disconnect(self):
        if self.isConnected:
            self.real_connection.disconnect()
            self.isConnected = False
            logger.info("Proxy desconectado de la base de datos real")
        else:
            logger.info("No hay conexión activa")

    def executeQuery(self, query):
        self.real_connection.executeQuery(query)

    def getCameras(self):

        cameras_from_db = self.real_connection.getCameras()

        return cameras_from_db

    def clearCache(self):
        """Método para limpiar la caché."""
        self.cache.clear()
        logger.info("Caché limpiada")

