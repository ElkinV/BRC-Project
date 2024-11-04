import pyodbc
from IDBConnection import IDBConnection
from cameras import Camera
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class SQLServerConnection(IDBConnection):
    def __init__(self, user: str, password: str, port: str, server: str, database: str):
        self.user = user
        self.password = password
        self.port = port
        self.server = server
        self.database = database
        self.conexion = None

    def connect(self):
        if not all([self.user, self.password, self.server, self.database]):
            logger.error("Los parámetros de conexión no están completos")
            return
        try:
            self.conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.user};'
                f'PWD={self.password}'
            )
            logger.info("Conexión exitosa a la base de datos")
        except pyodbc.Error as e:
            logger.error(f"Error al conectarse a la base de datos: {e}")

    def disconnect(self):
        if self.conexion:
            self.conexion.close()
            logger.info("Conexión cerrada")

    def executeQuery(self, query: str):
        try:
            if self.conexion:
                with self.conexion.cursor() as cursor:
                    cursor.execute(query)
                    self.conexion.commit()
                    logger.info(f"Consulta ejecutada: {query}")
            else:
                logger.warning("No hay conexión activa para ejecutar la consulta")
        except pyodbc.Error as e:
            logger.error(f"Error al ejecutar la consulta: {e}")

    def checkConnection(self) -> bool:
        try:
            if self.conexion:
                with self.conexion.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    cursor.fetchone()
                    return True
            else:
                logger.warning("No hay conexión activa")
                return False
        except pyodbc.Error as e:
            logger.error(f"Error al verificar la conexión: {e}")
            return False

    def getCameras(self) -> Optional[List[Camera]]:
        if not self.conexion:
            logger.warning("No hay conexión activa para obtener cámaras")
            return None
        try:
            with self.conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT top 1 camara_id, ip, usuario, clave, in1, in2, out1, out2
                    FROM API_camaras
                """)
                cameras = [
                    Camera(
                        id=fila[0], ip=fila[1], usuario=fila[2], clave=fila[3],
                        in1=fila[4], in2=fila[5], out1=fila[6], out2=fila[7]
                    )
                    for fila in cursor.fetchall()
                ]
                return cameras
        except pyodbc.Error as e:
            logger.error(f"Error al obtener cámaras: {e}")
            return None
