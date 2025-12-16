from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.get("/books")
def read_books():
    return [{"title": "Sample Book", "author": "Author Name"}]