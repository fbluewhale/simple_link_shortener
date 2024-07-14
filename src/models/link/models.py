import secrets,string
from datetime import datetime
from typing import Annotated, Optional
from enum import Enum
from beanie import Document, Indexed, Link
from pydantic.networks import HttpUrl
from pydantic.types import constr
from src.models.base import BaseDocument


class LinkDbModel(BaseDocument):

    original_link: HttpUrl
    shorten_path :Optional[constr(min_length=5, max_length=5)]=None
    name :constr(min_length=3, max_length=32)

    class Settings:
        name = "shorten_link"
        
    @classmethod
    async def generate_shorten_path(cls) -> str:
        links_count = await cls.all().count()
        if links_count >=len(string.ascii_letters + string.digits):
            raise Exception()
        while True:
            shorten_path = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(5))
            existing_link = await cls.find_one({"shorten_path": shorten_path})
            if not existing_link:
                return shorten_path

    async def insert(self, *args, **kwargs):
        self.shorten_path = await self.generate_shorten_path()
        await super().insert(*args, **kwargs)