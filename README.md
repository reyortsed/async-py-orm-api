# Async Python RestAPI Starter

A starter RestAPI using FastAPI, SQLite and SQLAlchemy Async extension. Supports OpenAPI Specification v3.1 / Swagger Docs

> Although I coded a bit in Python 5-6 years ago, this is my first serious adventure into the Python World, as I am, for the most part,
> a .NET C# developer.
> I have attempted to apply the design aspects of C# projects I have worked with, aswell as turning
> on as strict typing as possible with PyLance (thats what I am used to from the world of compiled languages)
> Any feedback in the form of comments / issues is appreciated. 
> Please feel free to fork the project for your own purposes.

## Features

- In this starter api, the following operations are supported (See Swagger Docs)
- Create User
- Read User
- Update User
- Delere User
- List All Users
- Test of Websocket features in FastAPI ASGI

## Tech
 - Python 3
 - PyTest
 - FastAPI (ASGI)
 - Swagger
 - SQLAlchemy 2.0 Async Extension
 - SQLite (Not limited to)

## Installation

### For a quick up and running dev version.

- Clone the repo
- Configure your python virtual env and activate
- run pip install -r requirements.txt
- Execute makecert.sh (requires shell with openssl). Generates a pub/priv pem and crt
- If you need a trusted certificate, install the cert.crt in Trusted Root Certificates
- The launch.json has a couple of configurations. One for regular debugging and one for a debug mode that supports attaching to process when using Websocket extension
- You can run the pytests in tests, or simply launch the project. Should work in both vscode or visual studio, but make sure you are using the correct venv
- Point your browser to https://localhost/docs for API
- Swagger docs should show
- Point your browser to https://localhost/wsclient for Websockets test (Note: when running with https, websocket must use wss protocol not ws, change the client connection string accordingly)

# Tests

- PyTests for most common API operations are performed
- Recommend installeing the Python Test Explorer in VSCode for better visualisation

# Hosting
- FastAPI with async functionality requires the Python ASGI module, which is not supported by all popular web servers
- For WebSocket support, you MUST use the uvicorn host.

## Standalone Servers supporting ASGI
 - Uvicorn
 - Hypercorn
 - Daphne
 - Gunicorn (with uvicorn.workers.UvicornWorker)
 - Trio-asyncio ASGI server (less common, experimental)
 - uvloop (via Uvicorn with --loop uvloop) – not a server itself but a performance-boosting event loop backend

## Cloud Platforms Supporting ASGI
 - You can host FastAPI async apps on:
 - AWS Lambda + API Gateway (with Mangum)
 - Azure App Service / Azure Functions (via ASGI adapters)
 - Google Cloud Run / App Engine
 - Heroku
 - Render
 - Fly.io
 - VPS with systemd or Docker

