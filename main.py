import requests
from fastapi import FastAPI, Response
from requests.auth import HTTPDigestAuth
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from asyncio import sleep
import uvicorn

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


camera_settings = {
    'URL': "http://181.48.82.11/stw-cgi/eventsources.cgi?msubmenu=peoplecount&action=check&Channel=0",
    'username': "admin",
    'password': "Aping.2024$"
}

header = {'Accept': 'application/json'}


session = requests.Session()
session.auth = HTTPDigestAuth(camera_settings["username"], camera_settings["password"])
session.headers.update(header)


async def camera_response():
    while True:
        try:
            response = session.get(camera_settings["URL"])
            response.raise_for_status()  # Asegura que la respuesta sea exitosa
            channels = response.json()['PeopleCount'][0]['Lines']

            for line in channels:
                yield f"event: PeopleCountingUpdate\ndata: {line}\n\n"
                await sleep(1)

        except requests.RequestException as e:
            yield f"event: Error\ndata: {str(e)}\n\n"
            await sleep(5)


@app.get("/stream-data")
async def stream_data():
    return StreamingResponse(camera_response(), media_type="text/event-stream")


@app.get("/get-data-once")
async def get_data_once():
    try:
        response = session.get(camera_settings["URL"])
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


@app.get("/")
async def root():
    return {"message": "API de conteo de personas activa"}

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.106", port=8000)
