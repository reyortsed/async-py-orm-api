import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",                   
        host="localhost",
        port=443,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem",
        reload=False
    )