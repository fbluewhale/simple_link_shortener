import logging
import importlib
import pkgutil

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.config import settings

import src.extensions
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.routes import router
from beanie import Document, Indexed, init_beanie
from src.models.base import BaseDocument
from src.schemas.general.error import BaseErrorInstance


def load_beanie_models(folder_dir):
    models = []
    # Ensure the folder path is absolute
    folder_dir = os.path.abspath(folder_dir)
    # Iterate over all subdirectories
    for root, dirs, files in os.walk(folder_dir):
        if "models.py" in files:
            # Construct the module path dynamically
            module_path = os.path.relpath(root, folder_dir).replace(os.path.sep, ".")
            module_name = (
                "src.models." + module_path + ".models"
                if module_path != "."
                else "models"
            )

            try:
                module = importlib.import_module(module_name)
                for attribute_name in dir(module):
                    attribute = getattr(module, attribute_name)
                    if (
                        isinstance(attribute, type)
                        and issubclass(attribute, Document)
                        and (
                            attribute is not Document and attribute is not BaseDocument
                        )
                    ):
                        models.append(attribute)
            except Exception as e:
                print(f"Error loading module {module_name}: {e}")

    return models


async def initialize_database():
    connection_string = os.getenv(
        "DATABASE_CONNECTION_STRING", "mongodb://localhost:27017"
    )
    client = AsyncIOMotorClient(connection_string, tz_aware=True)
    return client


async def initialize_odm(client):
    db_name = "link_shortener_test" if os.getenv("TESTING") else "link_shortener"

    await init_beanie(
        database=client.link_shortener_test if os.getenv("TESTING")else client.link_shortener, document_models=load_beanie_models("./src/models")
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await initialize_database()
    src.extensions.db = client[os.getenv("DATABASE", "link_shortener")]

    await initialize_odm(client)
    yield
    # await client.close()


app = FastAPI(    title=settings.title,
    version=settings.version,
    description=settings.description,
    openapi_prefix=settings.openapi_prefix,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
    lifespan=lifespan)
app.include_router(router)


app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "*").split(","),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ORIGINS", "*").split(","),
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from src.utilities.logger.formatters import LoggingMiddleware
from src.utilities.logger.log import RouterLoggingMiddleware

# Logger configuration
logger = logging.getLogger("request_logger")
logger.setLevel(logging.INFO)
from logging.handlers import RotatingFileHandler

# Log rotation setup
handler = RotatingFileHandler("logs/app.log", maxBytes=10000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

app.add_middleware(LoggingMiddleware, logger=logging.getLogger("request_logger"))


@app.exception_handler(Exception)
async def http_exception_handler(request, exc):
    error_instance = BaseErrorInstance(
        msg="something went wrong"
    ).model_dump()
    return JSONResponse(status_code=500, content={"detail": error_instance})

@app.get("/")
async def root():
    return {"message": "Link Shortener, Service is running..."}
