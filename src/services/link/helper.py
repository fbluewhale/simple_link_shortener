from bson.objectid import ObjectId
from fastapi import HTTPException

from src.models.link.models import LinkDbModel


async def delete_shorten_link(link_id: str):
    result = LinkDbModel.find_one(LinkDbModel.id == ObjectId(link_id))
    if await result.count() == 0:
        raise HTTPException(status_code=404, detail="Link not found")
    await result.delete()
