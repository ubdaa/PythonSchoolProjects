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
    book = await service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.patch("/{book_id}", response_model=BookRead)
async def update_book(
    book_id: int, book: BookUpdate, service: BookService = Depends()
):
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
    existing_book = await service.get_by_id(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await service.delete(book_id)
    return {"detail": "Book deleted successfully"}
