from datetime import datetime, timezone
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from app.auth.auth import verify_token
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

    # Add Bearer Auth security scheme to OpenAPI docs
    from fastapi.openapi.utils import get_openapi
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
        # Apply globally to all endpoints
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method.setdefault("security", []).append({"BearerAuth": []})
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    app.openapi = custom_openapi

    # Custom auth middleware
    @app.middleware("http")
    async def auth_middleware(request: Request, call_next):
        # Allow docs, openapi, and websocket endpoints without auth
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi") or request.url.path.startswith("/ws"):
            return await call_next(request)
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.lower().startswith("bearer "):
            return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
        token = auth_header.split(" ", 1)[1]
        try:
            user = verify_token(token)
            request.state.user = user
        except Exception as e:
            return JSONResponse(status_code=401, content={"detail": str(e)})
        return await call_next(request)

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
    
