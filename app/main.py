from fastapi import FastAPI
from app.database import engine, Base
from app.controllers import user_controller
import threading, webbrowser, time
from contextlib import asynccontextmanager
import uvicorn
from app.controllers import user_controller

def open_browser():
    time.sleep(1)
    webbrowser.open("https://localhost/docs")



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  

def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI(title="PiggyTail", version="1.0.0", lifespan=lifespan)
    
    # Load certificates, environment, logging only if not testing
    if not testing:
        # e.g., load_ssl_certs(), read_env(), etc.
        pass

    app.include_router(user_controller.router)
  
    return app


app = create_app()

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    uvicorn.run("main:app", host="localhost", port=443, reload=False, ssl_keyfile="key.pem", ssl_certfile="cert.pem" )
    
