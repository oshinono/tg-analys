from fastapi import FastAPI
from config import settings
from contextlib import asynccontextmanager
from client import client

@asynccontextmanager
async def lifespan(app: FastAPI):
    await client.start(settings.tg_phone, settings.tg_password)
    yield


app = FastAPI(root_path="/api",
              lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "приветики"}

@app.get("/health")
async def health():
    return {"status": "ok"}
