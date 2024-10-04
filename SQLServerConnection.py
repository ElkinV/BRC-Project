import pyodbc
from IDBConnection import IDBConnection
from cameras import Camera


class SQLServerConnection(IDBConnection):
    def __init__(self, user: str, password: str, port: str, server: str, database: str):
        self.user = user
        self.password = password
        self.port = port
        self.server = server
        self.database = database
        self.conexion = None

    def connect(self):
        try:
            # Crear la conexión con el servidor SQL Server
            self.conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                f'SERVER={self.server};'
                f'DATABASE={self.database};'
                f'UID={self.user};'
                f'PWD={self.password}'
            )
            print("Conexión exitosa a la base de datos")
        except pyodbc.Error as e:
            print("Error al conectarse a la base de datos:", e)

    def disconnect(self):
        if self.conexion:
            self.conexion.close()
            print("Conexión cerrada")

    def executeQuery(self, query: str):
        try:
            if self.conexion:
                cursor = self.conexion.cursor()
                cursor.execute(query)
                self.conexion.commit()
                print(f"Consulta ejecutada: {query}")
            else:
                print("No hay conexión activa para ejecutar la consulta")
        except pyodbc.Error as e:
            print("Error al ejecutar la consulta:", e)

    def checkConnection(self):
        try:
            if self.conexion:
                cursor = self.conexion.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
                return True
            else:
                print("No hay conexión activa")
                return False
        except pyodbc.Error as e:
            print("Error al verificar la conexión:", e)
            return False

    def getCameras(self):
        try:
            if self.conexion:
                cursor = self.conexion.cursor()
                # Consulta con los campos necesarios de la base de datos
                cursor.execute("""
                    SELECT TOP 2 camara_id, ip, usuario, clave, in1, in2, out1, out2 
                    FROM API_camaras
                """)  # Ajustar según la estructura de tu tabla

                cameras = []

                # Crear instancias de Camera con los datos obtenidos
                for fila in cursor.fetchall():
                    camera = Camera(
                        id=fila[0],
                        ip=fila[1],
                        usuario=fila[2],
                        clave=fila[3],
                        regla_1=fila[4],
                        in_1=fila[5],
                        regla_2=fila[6],
                        in_2=fila[7]
                    )
                    cameras.append(camera)

                return cameras  # Retornar lista de objetos Camera
            else:
                print("No hay conexión activa para obtener cámaras")
                return []
        except pyodbc.Error as e:
            print("Error al obtener cámaras:", e)
            return []