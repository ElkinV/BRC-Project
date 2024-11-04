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
        query = "SELECT camara_id, ip FROM API_camaras"

        if query in self.cache:
            logger.info("Comparando cámaras con la caché existente")

            cameras_from_db = self.real_connection.getCameras()
            cameras_in_cache = self.cache[query]

            if len(cameras_from_db) != len(cameras_in_cache):
                logger.info("El número de cámaras ha cambiado, actualizando la caché")
                self.cache[query] = cameras_from_db
            else:
                for camera_db, camera_cache in zip(cameras_from_db, cameras_in_cache):
                    if camera_db != camera_cache:
                        logger.info(f"La cámara con IP {camera_db.ip} ha cambiado, actualizando la caché")
                        self.cache[query] = cameras_from_db
                        break
                else:
                    logger.info("Las cámaras no han cambiado, devolviendo desde la caché")
                    return cameras_in_cache
        else:
            logger.info("Obteniendo cámaras desde la base de datos real")
            cameras_from_db = self.real_connection.getCameras()
            self.cache[query] = cameras_from_db

        return self.cache[query]

    def clearCache(self):
        """Método para limpiar la caché."""
        self.cache.clear()
        logger.info("Caché limpiada")

    def getCamerasByIP(self, camera_ip: str):
        query = f'SELECT camara_id, ip FROM API_camaras WHERE camara_id="{camera_ip}"'

        if query in self.cache:
            logger.info("Comparando cámaras con la caché existente")

            cameras_from_db = self.real_connection.getCameras()
            cameras_in_cache = self.cache[query]

            if len(cameras_from_db) != len(cameras_in_cache):
                logger.info("El número de cámaras ha cambiado, actualizando la caché")
                self.cache[query] = cameras_from_db
            else:
                for camera_db, camera_cache in zip(cameras_from_db, cameras_in_cache):
                    if camera_db != camera_cache:
                        logger.info(f"La cámara con IP {camera_db.ip} ha cambiado, actualizando la caché")
                        self.cache[query] = cameras_from_db
                        break
                else:
                    logger.info("Las cámaras no han cambiado, devolviendo desde la caché")
                    return cameras_in_cache
        else:
            logger.info("Obteniendo cámaras desde la base de datos real")
            cameras_from_db = self.real_connection.getCameras()
            self.cache[query] = cameras_from_db

        return self.cache[query]

