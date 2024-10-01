import requests
from fastapi import FastAPI
from requests.auth import HTTPDigestAuth

app = FastAPI()
CAMERA_API_URL = "http://181.48.82.11/stw-cgi/eventsources.cgi?msubmenu=peoplecount&action=check&Channel=0"
USERNAME = "admin"
PASSWORD = "Aping.2024$"
header = {'Accept':'application/json'}


@app.get("/")
async def root():
    response = requests.get(CAMERA_API_URL, auth=HTTPDigestAuth(USERNAME, PASSWORD), headers=header)
    response.raise_for_status()
    return response.json()
