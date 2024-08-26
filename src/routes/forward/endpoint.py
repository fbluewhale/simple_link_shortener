from fastapi import APIRouter, HTTPException
from pydantic.types import constr
from starlette.responses import RedirectResponse
from src.models.link.models import LinkDbModel
from src.services.link.helper import get_shorten_link_from_cache,set_shorten_link_in_cache

router_v1 = APIRouter(prefix="", tags=["forward"])


@router_v1.get("/{shorten_path}")
async def redirect_user(
    shorten_path: constr(min_length=5, max_length=5)
) -> RedirectResponse:
    # Check cache first
    cached_link = await get_shorten_link_from_cache(shorten_path)
    if cached_link:
        return RedirectResponse(cached_link["original_link"])

    # Cache miss, query the database
    shorten_link = await LinkDbModel.find_one({"shorten_path": shorten_path})
    if shorten_link:
        # Save the result in cache
        await set_shorten_link_in_cache(shorten_path, shorten_link)
        return RedirectResponse(shorten_link.original_link)
    else:
        raise HTTPException(status_code=404, detail="Shorten link not found")