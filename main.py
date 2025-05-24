from fastapi import FastAPI
from app.database import engine, Base
from app.controllers import user_controller
import threading, webbrowser, time
from contextlib import asynccontextmanager
import uvicorn

def open_browser():
    time.sleep(1)
    webbrowser.open("https://localhost/docs")

threading.Thread(target=open_browser).start()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  

app = FastAPI(title="PiggyTail", version="1.0.0", lifespan=lifespan)
from app.controllers import user_controller

app.include_router(user_controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=443, reload=False, ssl_keyfile="key.pem", ssl_certfile="cert.pem" )
