from fastapi import APIRouter, Depends, HTTPException, Query
from data.orm import SessionDep
from services.loan_service import LoanService
from schemas.loan import LoanCreate, LoanRead, LoanReturn
from schemas.common import PaginatedResponse
from data.models import LoanStatus

router = APIRouter(prefix="/loans", tags=["Loans"])


def get_loan_service(session: SessionDep) -> LoanService:
    return LoanService(session)


@router.post("/", response_model=LoanRead, status_code=201)
async def create_loan(
    loan: LoanCreate, service: LoanService = Depends(get_loan_service)
):
    try:
        return await service.create_loan(loan)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating loan: {str(e)}")


@router.get("/", response_model=PaginatedResponse[LoanRead])
async def list_loans(
    page: int = 1,
    page_size: int = 20,
    status: LoanStatus | None = None,
    borrower_mail: str | None = None,
    book_id: int | None = None,
    active_only: bool = False,
    late_only: bool = False,
    service: LoanService = Depends(get_loan_service),
):
    loans, total = await service.get_all_filtered(
        page=page,
        page_size=page_size,
        status=status,
        borrower_mail=borrower_mail,
        book_id=book_id,
        active_only=active_only,
        late_only=late_only,
    )

    total_pages = (total + page_size - 1) // page_size
    return PaginatedResponse(
        items=loans,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@router.get("/{loan_id}", response_model=LoanRead)
async def get_loan(loan_id: int, service: LoanService = Depends(get_loan_service)):
    return await service.get_loan_details(loan_id)


@router.post("/{loan_id}/return", response_model=LoanRead)
async def return_loan(
    loan_id: int,
    return_data: LoanReturn,
    service: LoanService = Depends(get_loan_service),
):
    return await service.return_loan(loan_id, return_data)


@router.post("/{loan_id}/renew", response_model=LoanRead)
async def renew_loan(loan_id: int, service: LoanService = Depends(get_loan_service)):
    return await service.renew_loan(loan_id)
