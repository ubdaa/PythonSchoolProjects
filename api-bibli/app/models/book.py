from pydantic import BaseModel
from typing import Optional as optional
from author import Author

# enum BookCategory
class BookCategory(str):
    FICTION = "Fiction"
    SCIENCE = "Science"
    HISTORY = "History"
    BIOGRAPHY = "Biography"
    CHILDREN = "Children"
    FANTASY = "Fantasy"

class Book(BaseModel):
    id: int
    title: str
    idbn: str
    year: int
    author: Author
    available_copies: int
    total_copies_owned: int
    description: str | None = None
    category: BookCategory
    language: str
    pages: int
    publisher: str