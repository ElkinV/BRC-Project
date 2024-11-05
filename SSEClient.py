import os
from ProxyDB import ProxyDB
from asyncio import sleep
import requests
import logging

from cameras import Camera

logger = logging.getLogger(__name__)

class SSEClient:
    def __init__(self, proxy: ProxyDB, buffer_size: int):
        self.proxy = proxy
        self.bufferSize = buffer_size
        self.is_streaming = False



    async def openStream(self):
        self.is_streaming = True

        # Obtener la lista de cámaras desde la base de datos mediante el ProxyDB
        db_cameras = self.proxy.getCameras()
        self.proxy.cache= db_cameras

        while self.is_streaming:
            for camera in db_cameras:
                try:
                    # Construir la URL específica para cada cámara usando su IP
                    camera_url = f"http://{camera.ip}/opensdk/WiseAI/search/objectcounting/check?channel=0&index=1&includeAIData=Live"

                    #Obtener usuario y clave de la camara en especifico
                    camera_user = camera.usuario
                    camera_password = camera.clave

                    session = requests.Session()
                    session.auth = requests.auth.HTTPDigestAuth(
                        camera_user, camera_password
                    )
                    session.headers.update({'Accept': 'application/json'})
                    response = session.get(camera_url)
                    response.raise_for_status()  # Asegura que la petición fue exitosa

                    # Obtener los datos de la respuesta JSON
                    lines = response.json()['objectCountingLive'][0]['countingRules'][0]["lines"]

                    cameraAPI = Camera()

                    cameraAPI.in1 = lines[0]['directionBasedResult'][0]['count']
                    cameraAPI.out1 = lines[0]['directionBasedResult'][1]['count']
                    cameraAPI.in2 = lines[1]['directionBasedResult'][0]['count']
                    cameraAPI.out2 = lines[1]['directionBasedResult'][1]['count']
                    # self.proxy.executeQuery(camera.to_sql_insert())

                    # Iterar sobre las líneas de conteo y enviarlas como eventos SSE
                    for line in lines:
                        # Enviar evento con los datos de conteo de personas por cámara
                        yield f"event: PeopleCountingUpdate\ndata: Cámara: {camera.ip} - {line['directionBasedResult']}\n\n"
                        await sleep(1)  # Pausar 1 segundo entre cada envío de datos


                    #insertar datos de camara en SQLserver
                    if camera != cameraAPI:
                        self.proxy.executeQuery(camera.to_sql_insert())
                    else:
                        continue
                except requests.RequestException as e:
                    # Si ocurre un error en la conexión, envía un evento de error y espera 5 segundos
                    logger.error(f"Error en la cámara {camera.ip}: {str(e)}")
                    yield f"event: Error\ndata: Error en la cámara {camera.ip}: {str(e)}\n\n"
                    await sleep(5)


    def APIcloseStream(self):
        """Método para cerrar el stream."""
        self.is_streaming = False
        logger.info("El stream ha sido cerrado.")
