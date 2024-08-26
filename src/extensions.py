import os
import redis

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from motor.core import AgnosticDatabase

from src.utilities.paginator.paginator import Paginator
from src.config import settings

class Client:
    db: AgnosticDatabase


db: AgnosticDatabase = None

paginator = Paginator()


def get_db():
    return db

redis_cache = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0, decode_responses=True)