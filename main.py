from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from SQLServerConnection import *
from starlette.responses import StreamingResponse
from ProxyDB import ProxyDB  # Asegúrate de que ProxyDB esté en el mismo directorio o ajusta la importación
from SSEClient import SSEClient  # Asegúrate de que SSEClient esté en el mismo directorio o ajusta la importación

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar la conexión a la base de datos y el ProxyDB
real_connection = SQLServerConnection(user="sa", password="10260411", port="", server="ELKIN-D\SQLEXPRESS", database="PeopleCounting")
proxy_db = ProxyDB(real_connection=real_connection, isConnected=False)

# Crear el cliente SSE
sse_client = SSEClient(proxy=proxy_db, buffer_size=10)

@app.on_event("startup")
async def startup_event():
    """Conectar a la base de datos al iniciar la aplicación."""
    proxy_db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Desconectar de la base de datos al cerrar la aplicación."""
    proxy_db.disconnect()

@app.get("/")
async def root():
    return {"message": "API de conteo de personas activa"}

@app.get("/stream-data")
async def stream_data():
    """Ruta para obtener el stream de conteo de personas de las cámaras."""
    return StreamingResponse(sse_client.openStream(), media_type="text/event-stream")

@app.post("/close-stream")
async def close_stream():
    """Ruta para cerrar el stream de conteo de personas."""
    sse_client.closeStream()
    return {"message": "El stream ha sido cerrado."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Cambia el host y puerto según tus necesidades
