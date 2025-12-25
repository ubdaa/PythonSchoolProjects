from pydantic import BaseModel, Field, field_validator, EmailStr, model_validator
from enum import Enum
import datetime


# Book models
class BookCategory(str, Enum):
    FICTION = "Fiction"
    SCIENCE = "Science"
    HISTORY = "History"
    BIOGRAPHY = "Biography"
    CHILDREN = "Children"
    FANTASY = "Fantasy"
    PHILOSOPHY = "Philosophy"


class BookBase(BaseModel):
    title: str
    isbn: str = Field(
        ..., pattern=r"^(97(8|9))?\d{9}(\d|X)$", description="ISBN-13 format"
    )
    year: int = Field(..., ge=1450, le=datetime.datetime.now().year)
    author_id: int
    available_copies: int = Field(..., ge=0)
    total_copies_owned: int = Field(..., ge=0)
    description: str | None = None
    category: BookCategory
    language: str = Field(
        ..., min_length=2, max_length=3, description="ISO country code"
    )
    pages: int = Field(..., gt=0)
    publisher: str

    @model_validator(mode="after")
    def check_copies(self):
        if self.available_copies > self.total_copies_owned:
            raise ValueError("Available copies cannot exceed total copies owned")
        return self

    @field_validator("language")
    def validate_language(cls, value):
        if len(value) not in (2, 3):
            raise ValueError("Language must be a 2 or 3 letter ISO country code")
        return value

    @field_validator("isbn")
    def validate_isbn(cls, value):
        clean_isbn = value.replace("-", "").replace(" ", "")
        if len(clean_isbn) != 13 or not clean_isbn.isdigit():
            raise ValueError("ISBN must be a valid ISBN-13 format")
        return clean_isbn


class BookRead(BookBase):
    id: int


class BookUpdate(BaseModel):
    title: str | None = None
    isbn: str | None = Field(
        None, pattern=r"^(97(8|9))?\d{9}(\d|X)$", description="ISBN-13 format"
    )
    year: int | None = Field(None, ge=1450, le=datetime.datetime.now().year)
    author_id: int | None = None
    available_copies: int | None = Field(None, ge=0)
    total_copies_owned: int | None = Field(None, ge=0)
    description: str | None = None
    category: BookCategory | None = None
    language: str | None = Field(
        None, min_length=2, max_length=3, description="ISO country code"
    )
    pages: int | None = Field(None, gt=0)
    publisher: str | None = None
