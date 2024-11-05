import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from SQLServerConnection import SQLServerConnection
from starlette.responses import StreamingResponse
from ProxyDB import ProxyDB  # Asegúrate de que ProxyDB esté en el mismo directorio o ajusta la importación
from SSEClient import SSEClient  # Asegúrate de que SSEClient esté en el mismo directorio o ajusta la importación
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Obtener configuración de la base de datos desde variables de entorno
load_dotenv()
db_user = os.getenv("DB_USER")
db_password =os.getenv("DB_PASSWORD")
db_server =os.getenv("DB_SERVER")
db_name = os.getenv("DB_NAME")

# Inicializar la conexión a la base de datos y el ProxyDB
real_connection = SQLServerConnection(user=db_user, password=db_password, port="", server=db_server, database=db_name)
proxy_db = ProxyDB(real_connection=real_connection, isConnected=False)

# Crear el cliente SSE
sse_client = SSEClient(proxy=proxy_db, buffer_size=10)

@app.on_event("startup")
async def startup_event():
    proxy_db.connect()
    logger.info("Aplicación iniciada y conectada a la base de datos")

@app.on_event("shutdown")
async def shutdown_event():
    """Desconectar de la base de datos al cerrar la aplicación."""
    proxy_db.disconnect()
    logger.info("Aplicación cerrada y desconectada de la base de datos")

@app.get("/")
async def root():
    return {"message": "API de conteo de personas activa"}

@app.get("/stream-data")
async def stream_data():
    """Ruta para obtener el stream de conteo de personas de las cámaras."""
    logger.info("Iniciando stream de datos")
    return StreamingResponse(sse_client.openStream(), media_type="text/event-stream")

@app.post("/close-stream")
async def close_stream():
    """Ruta para cerrar el stream de conteo de personas."""
    sse_client.closeStream()
    logger.info("Stream de datos cerrado")
    return {"message": "El stream ha sido cerrado."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Cambia el host y puerto según tus necesidades
