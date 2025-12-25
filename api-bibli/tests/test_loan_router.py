from unittest.mock import AsyncMock
from fastapi import FastAPI
from fastapi.testclient import TestClient
from datetime import date
from app.main import app
from app.routers.loan_router import router
from app.services.loan_service import LoanService
from app.schemas.loan import LoanRead
from app.data.models import LoanStatus

app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_create_loan():
    mock_service = AsyncMock()
    mock_loan = LoanRead(
        id=1, book_id=1, borrower_email="test@example.com", 
        loan_date=date.today(), return_date=None, status=LoanStatus.ACTIVE
    )
    mock_service.create_loan.return_value = mock_loan
    app.dependency_overrides[LoanService] = lambda: mock_service

    response = client.post("/loans/", json={"book_id": 1, "borrower_email": "test@example.com"})
    assert response.status_code == 201
    assert response.json()["id"] == 1

def test_list_loans():
    mock_service = AsyncMock()
    mock_service.get_all_filtered.return_value = ([], 0)
    app.dependency_overrides[LoanService] = lambda: mock_service

    response = client.get("/loans/")
    assert response.status_code == 200
    assert response.json()["items"] == []

def test_return_loan():
    mock_service = AsyncMock()
    mock_loan = LoanRead(
        id=1, book_id=1, borrower_email="test@example.com", 
        loan_date=date.today(), return_date=date.today(), status=LoanStatus.RETURNED
    )
    mock_service.return_loan.return_value = mock_loan
    app.dependency_overrides[LoanService] = lambda: mock_service

    response = client.post("/loans/1/return", json={"condition": "Good"})
    assert response.status_code == 200
    assert response.json()["status"] == "RETURNED"
