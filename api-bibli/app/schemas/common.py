from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int

class StatsResponse(BaseModel):
    total_books: int
    total_authors: int
    total_loans: int
    active_loans: int
    late_loans: int
    occupancy_rate: float
    
class BookStatsResponse(BaseModel):
    book_id: int
    book_title: str
    total_loans: int
    average_loan_duration: float
    times_late: int
    popularity_rank: Optional[int] = None
    
class AuthorStatsResponse(BaseModel):
    author_id: int
    author_name: str
    total_books: int
    total_loans: int