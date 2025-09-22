import math
from dataclasses import dataclass, field


@dataclass(kw_only=True, slots=True)
class Pagination:
    page: int = field(default=1)
    page_size: int = field(default=10)

    @property
    def limit_offset(self) -> tuple[int, int]:
        offset = (max(self.page, 1) - 1) * self.page_size
        limit = self.page_size
        return limit, offset


@dataclass(kw_only=True, slots=True)
class PaginationResult:
    page: int
    page_size: int
    count: int
    total_count: int
    total_pages: int

    @classmethod
    def from_pagination(
        cls, pagination: Pagination, count: int, total_count: int
    ) -> "PaginationResult":
        total_pages = math.ceil(total_count / pagination.page_size)
        return cls(
            page=pagination.page,
            page_size=pagination.page_size,
            count=count,
            total_count=total_count,
            total_pages=total_pages,
        )
