import asyncio
from datetime import datetime
from typing import Optional, TypeVar, Type
from pydantic import Field

from beanie import Document

T = TypeVar("T", bound="BaseDocument")


class BaseDocument(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow, title="Creation Time")
    modified_at: datetime = Field(
        default_factory=datetime.utcnow, title="Modification Time"
    )

    @classmethod
    async def get_or_create(cls: Type[T], **kwargs) -> T:
        # Prepare filter query based on unique fields
        filter_query = {key: kwargs[key] for key in kwargs if "__" not in key}
        instance = await cls.find_one(filter_query)
        if not instance:
            # Instance does not exist, so create it
            instance = cls(**kwargs)
            await instance.insert()
            # Make sure to set created_at and modified_at upon creation
            instance.created_at = datetime.utcnow()
            instance.modified_at = datetime.utcnow()
            await instance.save()
        return instance

    # Overriding the save method to update 'modified_at' every time the document is saved
    async def save(self, *args, **kwargs):
        self.modified_at = datetime.utcnow()
        await super().save(*args, **kwargs)

    @classmethod
    async def get_or_create(cls, **kwargs):
        instance = await cls.find_one(kwargs)
        if not instance:
            instance = cls(**kwargs)
            await instance.insert()
        return instance
