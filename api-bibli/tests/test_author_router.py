from unittest.mock import AsyncMock, MagicMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app.routers.author_router import router
from app.services.author_service import AuthorService
from app.schemas.author import AuthorRead

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_list_authors():
    mock_service = AsyncMock()
    mock_service.get_all_filtered.return_value = ([], 0)
    app.dependency_overrides[AuthorService] = lambda: mock_service

    response = client.get("/authors/")
    assert response.status_code == 200
    assert response.json()["items"] == []

def test_create_author():
    mock_service = AsyncMock()
    mock_service.get_by_fullname.return_value = None
    mock_service.add.return_value = AuthorRead(id=1, first_name="John", last_name="Doe", date_of_birth="1970-01-01", nationality="USA")
    app.dependency_overrides[AuthorService] = lambda: mock_service

    response = client.post("/authors/", json={"first_name": "John", "last_name": "Doe", "date_of_birth": "1970-01-01", "nationality": "USA"})
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"

def test_get_author():
    mock_service = AsyncMock()
    mock_service.get_by_id.return_value = AuthorRead(id=1, first_name="John", last_name="Doe", date_of_birth="1970-01-01", nationality="USA")
    app.dependency_overrides[AuthorService] = lambda: mock_service

    response = client.get("/authors/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_delete_author():
    mock_service = AsyncMock()
    mock_service.get_by_id.return_value = MagicMock()
    mock_service.delete.return_value = None
    app.dependency_overrides[AuthorService] = lambda: mock_service

    response = client.delete("/authors/1")
    assert response.status_code == 200
