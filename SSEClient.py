import os
from ProxyDB import ProxyDB
from asyncio import sleep
import requests
import logging

logger = logging.getLogger(__name__)

class SSEClient:
    def __init__(self, proxy: ProxyDB, buffer_size: int):
        self.proxy = proxy
        self.bufferSize = buffer_size
        self.is_streaming = False

        # Obtener credenciales desde variables de entorno
        self.camera_user = os.getenv("CAMERA_USER", "admin")
        self.camera_password = os.getenv("CAMERA_PASSWORD", "Aping.2024$")

        self.session = requests.Session()
        self.session.auth = requests.auth.HTTPDigestAuth(
            self.camera_user, self.camera_password
        )
        self.session.headers.update({'Accept': 'application/json'})

    async def openStream(self):
        """Método para abrir el stream de eventos y enviar actualizaciones para cada cámara."""
        self.is_streaming = True

        # Obtener la lista de cámaras desde la base de datos mediante el ProxyDB
        db_cameras = self.proxy.getCameras()

        while self.is_streaming:
            for camera in db_cameras:
                try:
                    # Construir la URL específica para cada cámara usando su IP
                    camera_url = f"http://{camera.ip}/opensdk/WiseAI/search/objectcounting/check?channel=0&index=1&includeAIData=Live"

                    # Hacer la petición a la API de cada cámara
                    response = self.session.get(camera_url)
                    response.raise_for_status()  # Asegura que la petición fue exitosa

                    # Obtener los datos de la respuesta JSON
                    lines = response.json()['objectCountingLive'][0]['countingRules'][0]["lines"]

                    camera.in1 = lines[0]['directionBasedResult'][0]['count']
                    camera.out1 = lines[1]['directionBasedResult'][0]['count']
                    camera.in2 = lines[0]['directionBasedResult'][1]['count']
                    camera.out2 = lines[1]['directionBasedResult'][1]['count']
                    # self.proxy.executeQuery(camera.to_sql_insert())

                    # Iterar sobre las líneas de conteo y enviarlas como eventos SSE
                    for line in lines:
                        # Enviar evento con los datos de conteo de personas por cámara
                        yield f"event: PeopleCountingUpdate\ndata: Cámara: {camera.ip} - {line['directionBasedResult']}\n\n"
                        await sleep(1)  # Pausar 1 segundo entre cada envío de datos

                except requests.RequestException as e:
                    # Si ocurre un error en la conexión, envía un evento de error y espera 5 segundos
                    logger.error(f"Error en la cámara {camera.ip}: {str(e)}")
                    yield f"event: Error\ndata: Error en la cámara {camera.ip}: {str(e)}\n\n"
                    await sleep(5)

            # Consultar nuevamente la base de datos y comparar las cámaras con la caché
            new_db_cameras = self.proxy.getCameras()


            if new_db_cameras[0] != db_cameras[0]:
                logger.info("Las cámaras han cambiado, actualizando la lista.")
                db_cameras = new_db_cameras  # Actualiza la lista de cámaras

            if camera in new_db_cameras:
                print(camera, db_cameras)

    def closeStream(self):
        """Método para cerrar el stream."""
        self.is_streaming = False
        logger.info("El stream ha sido cerrado.")
