from datetime import datetime, timezone
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from app.database import engine, Base
from app.controllers import user_controller
from app.controllers import course_controller
import threading, webbrowser, time
from contextlib import asynccontextmanager
import uvicorn
from typing import List

def open_browser():
    time.sleep(1)
    webbrowser.open("https://localhost/docs")

# Manage connected clients
connected_clients: List[WebSocket] = []

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
    app.include_router(course_controller.router)

    return app    

app = create_app()

@app.get("/wsclient")
async def get():
    return HTMLResponse("""
    <html>
        <body>
            <h1>WebSocket Test</h1>
            <script>
                const ws = new WebSocket("wss://localhost/ws");
                ws.onmessage = event => {
                    const message = event.data;
                    const p = document.createElement("p");
                    p.textContent = "Received: " + message;
                    document.body.appendChild(p);
                };

                setInterval(() => {
                    ws.send("Hello from client at " + new Date().toLocaleTimeString());
                }, 3000);
            </script>
        </body>
    </html>
    """)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received: {data}")
            for client in connected_clients:
                await client.send_text(f"{data}")
                time.sleep(2)
                await client.send_text(f"I took 2 seconds to read your message :) Hello from server at {datetime.now(timezone.utc).isoformat()}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
   
    uvicorn.run(
        "main:app",          
        host="localhost",
        port=443,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem",
        reload=False
    )
    
