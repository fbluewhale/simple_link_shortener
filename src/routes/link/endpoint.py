from typing import List, Annotated

from starlette.types import Message
from src.models.link.models import LinkDbModel
from src.schemas.general.error import BaseErrorInstance
from src.schemas.general.request import PaginateQueryParams
from src.schemas.general.response import WithMessageResponse
from src.services.link.helper import delete_shorten_link
from src.utilities.paginator.paginator import Paginator
from src.extensions import paginator

from fastapi import APIRouter, Body, Query, Depends

from src.schemas.link.request import LinkCreateRequest
from src.schemas.link.response import LinkPaginatedResponse

router_v1 = APIRouter(prefix="/api/v1/link", tags=["link"])


@router_v1.post(
    "/", responses={400: {"model": BaseErrorInstance}}, response_model=LinkDbModel
)
async def create_shorten_path(link_data: LinkCreateRequest = Body(...)):
    new_link = LinkDbModel(**link_data.model_dump())
    await new_link.insert()
    return new_link


@router_v1.get("/")
async def get_shorten_links(
    paginate: Annotated[dict, Depends(PaginateQueryParams)],
) -> LinkPaginatedResponse:
    shorten_links = LinkDbModel.all()
    return await paginator.paginate(shorten_links, paginate.per_page, paginate.page)


@router_v1.delete("/{link_id}/")
async def delete_shorten_link_api(link_id: str):
    await delete_shorten_link(link_id)
    return WithMessageResponse(msg=f"Link with id {link_id} has been deleted")
