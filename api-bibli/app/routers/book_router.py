from fastapi import APIRouter, HTTPException, Depends, Query
from schemas.common import PaginatedResponse
from data.orm import Book as BookORM
from services.book_service import BookService
from schemas.book import BookRead, BookBase, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=PaginatedResponse[BookRead])
async def list_books(
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    category: str | None = None,
    language: str | None = None,
    sort_by: str = Query("title", regex="^(title|year|author_id)$"),
    order: str = Query("asc", regex="^(asc|desc)$"),
    service: BookService = Depends(),
):
    """
    Retrieve a paginated list of books with optional filtering and sorting.

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20)
    - **search**: Search term for book title or author
    - **category**: Filter by category
    - **language**: Filter by language
    - **sort_by**: Sort by field (title, year, or author_id)
    - **order**: Sort order (asc or desc)
    """
    items, total = await service.get_all_filtered(
        page=page,
        page_size=page_size,
        search=search,
        category=category,
        language=language,
        sort_by=sort_by,
        order=order,
    )
    total_pages = (total + page_size - 1) // page_size
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.post("/", response_model=BookRead)
async def create_book(book: BookBase, service: BookService = Depends()):
    """
    Create a new book.

    - **book**: Book data to create
    """
    try:
        existing = await service.get_by_isbn(book.isbn)
        if existing:
            raise HTTPException(
                status_code=400, detail="Book with this ISBN already exists"
            )

        db_book = BookORM(**book.model_dump())
        created_book = await service.add(db_book)
        return created_book
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating book: {str(e)}")


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, service: BookService = Depends()):
    """
    Retrieve a book by ID.

    - **book_id**: The ID of the book to retrieve
    """
    book = await service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: int, book: BookUpdate, service: BookService = Depends()
):
    """
    Update an existing book.

    - **book_id**: The ID of the book to update
    - **book**: Updated book data
    """
    existing_book = await service.get_by_id(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    existing = await service.get_by_isbn(book.isbn)
    if existing and existing.id != book_id:
        raise HTTPException(
            status_code=400, detail="Book with this ISBN already exists"
        )

    old_book = existing_book

    for key, value in book.model_dump().items():
        if value is not None:
            setattr(existing_book, key, value)

    if old_book.isbn != existing_book.isbn:
        existing = await service.get_by_isbn(existing_book.isbn)
        if existing:
            raise HTTPException(
                status_code=400, detail="Book with this ISBN already exists"
            )

    updated_book = await service.update(existing_book)
    return updated_book


@router.delete("/{book_id}")
async def delete_book(book_id: int, service: BookService = Depends()):
    """
    Delete a book by ID.

    - **book_id**: The ID of the book to delete
    """
    existing_book = await service.get_by_id(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await service.delete(book_id)
    return {"detail": "Book deleted successfully"}
