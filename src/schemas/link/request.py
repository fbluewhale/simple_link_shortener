from pydantic import BaseModel
from pydantic.networks import HttpUrl


class LinkCreateRequest(BaseModel):
    original_link: HttpUrl
    name: str
