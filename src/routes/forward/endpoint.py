from typing import Union
from fastapi import APIRouter, HTTPException
from pydantic.types import constr
from starlette.responses import RedirectResponse
from src.models.link.models import LinkDbModel

router_v1 = APIRouter(prefix="", tags=["forward"])


@router_v1.get("/{shorten_path}")
async def redirect_user(
    shorten_path: constr(min_length=5, max_length=5)
) -> RedirectResponse:
    shorten_link = await LinkDbModel.find_one({"shorten_path": shorten_path})
    if shorten_link:
        return RedirectResponse(shorten_link.original_link)
    else:
        raise HTTPException(status_code=404, detail="Shorten link not found")
