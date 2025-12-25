from fastapi import APIRouter, HTTPException, Depends, Query
from app.schemas.common import PaginatedResponse
from app.services.author_service import AuthorService
from app.data.orm import Author as AuthorORM
from app.schemas.author import AuthorBase, AuthorRead, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", response_model=PaginatedResponse[AuthorRead])
async def list_authors(
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
    nationality: str | None = None,
    sort_by: str = Query("last_name", pattern="^(last_name|first_name|birth_date)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    service: AuthorService = Depends(),
):
    """
    Retrieve a paginated list of authors with optional filtering and sorting.

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20)
    - **search**: Search term for author's name
    - **nationality**: Filter by nationality
    - **sort_by**: Sort by field (last_name, first_name, or birth_date)
    - **order**: Sort order (asc or desc)
    """
    try:
        authors, total = await service.get_all_filtered(
            page=page,
            page_size=page_size,
            search=search,
            nationality=nationality,
            sort_by=sort_by,
            order=order,
        )
        total_pages = (total + page_size - 1) // page_size
        return PaginatedResponse(
            items=authors,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error listing authors: {str(e)}")


@router.post("/", response_model=AuthorRead)
async def create_author(
    author: AuthorBase, service: AuthorService = Depends()
):
    """
    Create a new author.

    - **author**: Author data to create
    """
    try:
        existing = await service.get_by_fullname(author.first_name, author.last_name)
        if existing:
            raise HTTPException(
                status_code=400, detail="Author with this name already exists"
            )

        db_author = AuthorORM(**author.model_dump())
        created_author = await service.add(db_author)
        return created_author
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating author: {str(e)}")


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author(
    author_id: int, service: AuthorService = Depends()
):
    """
    Retrieve an author by ID.

    - **author_id**: The ID of the author to retrieve
    """
    author = await service.get_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=AuthorRead)
async def update_author(
    author_id: int,
    author: AuthorUpdate,
    service: AuthorService = Depends(),
):
    """
    Update an existing author.

    - **author_id**: The ID of the author to update
    - **author**: Updated author data
    """
    existing_author = await service.get_by_id(author_id)
    if not existing_author:
        raise HTTPException(status_code=404, detail="Author not found")

    existing = await service.get_by_fullname(author.first_name, author.last_name)
    if existing:
        raise HTTPException(
            status_code=400, detail="Author with this name already exists"
        )

    for key, value in author.model_dump().items():
        if value is not None:
            setattr(existing_author, key, value)
    updated_author = await service.update(existing_author)
    return updated_author


@router.delete("/{author_id}")
async def delete_author(
    author_id: int, service: AuthorService = Depends()
):
    """
    Delete an author by ID.

    - **author_id**: The ID of the author to delete
    """
    existing_author = await service.get_by_id(author_id)
    if not existing_author:
        raise HTTPException(status_code=404, detail="Author not found")
    await service.delete(author_id)
    return {"detail": "Author deleted successfully"}
