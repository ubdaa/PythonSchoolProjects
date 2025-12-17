from pydantic import BaseModel, Field, field_validator, EmailStr, model_validator
from enum import Enum
import datetime
from schemas.author import Author

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
    title: str
    isbn: str = Field(..., pattern=r'^(97(8|9))?\d{9}(\d|X)$', description="ISBN-13 format")
    year: int = Field(..., ge=1450, le=datetime.datetime.now().year)
    author_id: int
    available_copies: int = Field(..., ge=0)
    total_copies_owned: int = Field(..., ge=0)
    description: str | None = None
    category: BookCategory
    language: str = Field(..., min_length=2, max_length=3, description="ISO country code")
    pages: int = Field(..., gt=0)
    publisher: str

    @model_validator(mode='after')
    def check_copies(self):
        if self.available_copies > self.total_copies_owned:
            raise ValueError('Available copies cannot exceed total copies owned')
        return self
    