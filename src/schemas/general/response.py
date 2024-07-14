from pydantic import BaseModel, Field


class WithMessageResponse(BaseModel):
    msg: str


class PaginatedResponse(BaseModel):
    total: int = 0
    per_page: int = 0
    current_page: int = 0
    last_page: int = 0
    data: list | None
