from pydantic import BaseModel, Field, EmailStr, model_validator
from enum import Enum
import datetime


# Author model
class Author(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    date_of_death: datetime.date | None = None
    nationality: str = Field(
        ..., min_length=2, max_length=3, description="ISO country code"
    )
    biography: str | None = None
    website: str | None = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.date_of_death and self.date_of_death < self.date_of_birth:
            raise ValueError("Date of death must be after date of birth")
        return self


# Book models
class BookCategory(str, Enum):
    FICTION = "Fiction"
    SCIENCE = "Science"
    HISTORY = "History"
    BIOGRAPHY = "Biography"
    CHILDREN = "Children"
    FANTASY = "Fantasy"
    PHILOSOPHY = "Philosophy"


class Book(BaseModel):
    id: int
    title: str
    isbn: str = Field(
        ..., pattern=r"^(97(8|9))?\d{9}(\d|X)$", description="ISBN-13 format"
    )
    year: int = Field(..., ge=1450, le=datetime.datetime.now().year)
    author: Author
    available_copies: int = Field(..., ge=0)
    total_copies_owned: int = Field(..., ge=0)
    description: str | None = None
    category: BookCategory
    language: str
    pages: int = Field(..., gt=0)
    publisher: str

    @model_validator(mode="after")
    def check_copies(self):
        if self.available_copies > self.total_copies_owned:
            raise ValueError("Available copies cannot exceed total copies owned")
        return self


# Loan models
class LoanStatus(str, Enum):
    ON_LOAN = "On Loan"
    RETURNED = "Returned"
    OVERDUE = "Overdue"


class Loan(BaseModel):
    id: int
    book_id: int
    borrower_name: str
    borrower_mail: EmailStr
    card_number: str
    loan_date: datetime.datetime
    due_date: datetime.datetime
    return_date: datetime.datetime | None = None
    status: LoanStatus
    comments: str | None = None

    @model_validator(mode="after")
    def check_return_date(self):
        if self.return_date and self.return_date < self.loan_date:
            raise ValueError("Return date must be after loan date")
        return self


# Loan History model
class LoanHistory(BaseModel):
    id: int
    book_id: int
    total_loans: int = 0
    average_duration_days: float = 0.0
    popularity_score: int = 0
