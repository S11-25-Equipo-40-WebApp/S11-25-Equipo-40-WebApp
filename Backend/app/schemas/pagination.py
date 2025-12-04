from typing import TypeVar

from sqlmodel import SQLModel

T = TypeVar("T")


class PaginationResponse[T](SQLModel):
    total_items: int
    page: int
    size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    results: list[T]
