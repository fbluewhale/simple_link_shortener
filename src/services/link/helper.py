import json
from typing import Union
from bson.objectid import ObjectId
from fastapi import HTTPException

from src.models.link.models import LinkDbModel
from src.extensions import redis_cache
from src.config import settings

async def delete_shorten_link(link_id: str):
    result = LinkDbModel.find_one(LinkDbModel.id == ObjectId(link_id))
    if await result.count() == 0:
        raise HTTPException(status_code=404, detail="Link not found")
    await result.delete()

async def get_shorten_link_from_cache(shorten_path: str) -> Union[dict, None]:
    cached_data = redis_cache.get(shorten_path)
    if cached_data:
        return json.loads(cached_data)
    return None

async def set_shorten_link_in_cache(shorten_path: str, shorten_link: LinkDbModel):
    redis_cache.setex(shorten_path, settings.CACHE_TTL, shorten_link.model_dump_json())
