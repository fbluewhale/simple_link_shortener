from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from motor.core import AgnosticDatabase

from src.utilities.paginator.paginator import Paginator

# class Database:
#     client: AsyncIOMotorClient = None


# class Client:
#     db: AsyncIOMotorDatabase = None


# client = Client()
class Client:
    db: AgnosticDatabase


db: AgnosticDatabase = None

paginator = Paginator()


def get_db():
    return db
