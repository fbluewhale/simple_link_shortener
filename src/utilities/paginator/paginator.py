from math import ceil
from src.schemas.general.response import PaginatedResponse


class Paginator:

    def __init__(self, per_page=10):
        self.per_page = per_page

    def __calc_start_and_end(self, page, item_total_count, per_page):
        start_item = (page - 1) * per_page
        end_item = start_item + per_page
        last_page = ceil(item_total_count / per_page)
        return start_item, end_item, last_page

    async def paginate(self, query, per_page, page=1):
        per_page = per_page or self.per_page
        total_count = await query.count()
        start_item, end_item, last_page = self.__calc_start_and_end(
            page, total_count, per_page
        )

        return PaginatedResponse(
            total=total_count,
            per_page=per_page,
            current_page=page,
            last_page=last_page,
            data=await query.skip(start_item).limit(end_item - start_item).to_list(),
        )
