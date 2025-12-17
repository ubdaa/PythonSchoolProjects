from fastapi import APIRouter, HTTPException, Depends
from demo_etu.app.schemas.common import PaginatedResponse
from services.author_service import AuthorService
from data.orm import SessionDep, Author as AuthorORM
from schemas.author import AuthorBase

router = APIRouter(prefix="/authors", tags=["Authors"])

def get_author_service(session: SessionDep) -> AuthorService:
    return AuthorService(session)

@router.get("/", response_model=PaginatedResponse[AuthorBase])
async def list_authors(
    page: int = 1,
    page_size: int = 20,
    search: str | None = None,
):
    pass

@router.post("/", response_model=AuthorBase)
async def create_author(author: AuthorBase, service: AuthorService = Depends(get_author_service)):
    try:
        existing = await service.get_by_fullname(author.first_name, author.last_name)
        if existing:
            raise HTTPException(status_code=400, detail="Author with this name already exists")
        
        db_author = AuthorORM(**author.model_dump())
        created_author = await service.add(db_author)
        return created_author
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating author: {str(e)}")

@router.get("/{author_id}")
async def get_author(author_id: int, service: AuthorService = Depends(get_author_service)):
    author = await service.get_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author
