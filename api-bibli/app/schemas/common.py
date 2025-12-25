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

class MonthlyReportResponse(BaseModel):
    month: str
    new_books: int
    new_users: int
    total_loans: int
    returned_loans: int

class UserActivityResponse(BaseModel):
    user_id: int
    full_name: str
    total_loans: int
    current_loans: int
    late_returns: int

class NeverBorrowedBookResponse(BaseModel):
    book_id: int
    title: str
    added_date: str