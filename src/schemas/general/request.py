from datetime import date
from typing import Optional
from fastapi import Depends, FastAPI, Query


class PaginateQueryParams:
    def __init__(self, page: int = 1, per_page: int = Query(10, gt=0, le=100)):
        self.page = page
        self.per_page = per_page


class DateFilter:
    def __init__(
        self,
        from_date: Optional[date] = Query(
            None, description="Start date for filtering (inclusive)."
        ),
        to_date: Optional[date] = Query(
            None, description="End date for filtering (inclusive)."
        ),
    ):
        self.from_date = from_date
        self.to_date = to_date
