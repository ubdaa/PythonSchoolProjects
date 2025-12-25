from unittest.mock import AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from app.routers.stats_router import router, get_service

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_get_statistics():
    mock_service = AsyncMock()
    mock_service.get_global_stats.return_value = {
        "total_books": 100,
        "total_authors": 50,
        "active_loans": 10,
        "total_loans": 200,
        "late_loans": 5,
        "occupancy_rate": 0.1
    }
    app.dependency_overrides[get_service] = lambda: mock_service

    response = client.get("/stats/")
    assert response.status_code == 200
    assert response.json()["total_books"] == 100

def test_get_book_statistics():
    mock_service = AsyncMock()
    mock_service.get_book_stats.return_value = {
        "book_id": 1,
        "book_title": "Test Book",
        "total_loans": 5,
        "current_loans": 1,
        "average_loan_duration": 7.5,
        "times_late": 2
    }
    app.dependency_overrides[get_service] = lambda: mock_service

    response = client.get("/stats/books/1")
    assert response.status_code == 200
    assert response.json()["book_title"] == "Test Book"

def test_export_csv():
    mock_service = AsyncMock()
    mock_service.get_global_stats.return_value = {"total_books": 10}
    app.dependency_overrides[get_service] = lambda: mock_service

    response = client.get("/stats/export/csv")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/csv; charset=utf-8"
