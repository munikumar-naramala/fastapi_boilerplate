import logging
import click
import uvicorn

from fastapi import FastAPI, Depends
from app.config import settings
from starlette.middleware.cors import CORSMiddleware
from app.api.endpoints.api import api_router
from app.api.deps import authenticate
from app.backend_pre_start import main
from app.db.session import engine

from app import models

# Create the tables if not available in models
models.Base.metadata.create_all(bind=engine)


logger = logging.getLogger(settings.PROJECT_NAME)
app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"/openapi.json")

# Set all CORS enabled origins
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(api_router, prefix=settings.API, dependencies=[Depends(authenticate)])


@app.on_event("startup")
def startup_events():
    main()


@app.on_event("shutdown")
def shutdown_event():
    # Note: Can add closing DB connections adn checking message queues
    click.echo('Exiting the Management System')


@click.group()
def cli():
    """ Entry point for the application functions. """
    pass


@cli.command()
def run():
    """
    Start the fastAPI Micro Service
    """
    uvicorn.run(app, host='0.0.0.0', port=settings.APPLICATION_PORT)
