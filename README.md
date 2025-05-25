# Async Python RestAPI Starter

A starter RestAPI using FastAPI, SQLite and SQLAlchemy Async extension. Supports OpenAPI Specification v3.1 / Swagger Docs

> This is my first serious adventure into the Python World, as I am in essence a .NET C# developer. > I have attempted to apply the design aspects of C# projects I have worked with, aswell as turning > on as strict typing as possible with PyLance (thats what I am used to)
> Any feedback in the form of comments / issues is appreciated. 
> Please feel free to fork the project for your own purposes.
## Features

- In this starter api, the following operations are supported (See Swagger Docs)
- Create User
- Read User
- Update User
- Delere User
- List All Users

## Tech
 - Python 3
 - FastAPI
 - Swagger
 - SQLAlchemy 2.0 Async Extension
 - SQLite (Not limited to)

## Installation
-- For a quick up and running dev version.
- Clone the repo
- Configure your python virtual env and activate
- run pip install -r requirements.txt
- Execute makecert.sh (requires shell with openssl). Generates a pub/priv pem and crt
- Install the cert.crt in Trusted Root Certificates
- Run main.py
- Point your browser to https://localhost/docs
- Swagger docs should show

# Hosting
- FastAPI with async functionality requires the Python ASGI module, which is not supported by all popular web servers

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

