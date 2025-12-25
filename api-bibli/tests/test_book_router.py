from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app.routers.book_router import router
from app.services.book_service import BookService
from app.schemas.book import BookRead

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_list_books():
    mock_service = AsyncMock()
    mock_service.get_all_filtered.return_value = ([], 0)
    
    app.dependency_overrides[BookService] = lambda: mock_service

    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0

def test_create_book():
    mock_service = AsyncMock()
    mock_service.get_by_isbn.return_value = None
    mock_service.add.return_value = BookRead(id=1, title="Test Book", isbn="123", author_id=1, year=2023, available_copies=5)
    app.dependency_overrides[BookService] = lambda: mock_service

    response = client.post("/books/", json={"title": "Test Book", "isbn": "123", "author_id": 1, "year": 2023, "available_copies": 5})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_get_book_not_found():
    mock_service = AsyncMock()
    mock_service.get_by_id.return_value = None
    app.dependency_overrides[BookService] = lambda: mock_service

    response = client.get("/books/999")
    assert response.status_code == 404

def test_delete_book():
    mock_service = AsyncMock()
    mock_service.get_by_id.return_value = MagicMock()
    mock_service.delete.return_value = None
    app.dependency_overrides[BookService] = lambda: mock_service

    response = client.delete("/books/1")
    assert response.status_code == 200
