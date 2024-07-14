from typing import List
from src.models.link.models import LinkDbModel
from src.schemas.general.response import PaginatedResponse


class LinkPaginatedResponse(PaginatedResponse):
    data: List[LinkDbModel]
