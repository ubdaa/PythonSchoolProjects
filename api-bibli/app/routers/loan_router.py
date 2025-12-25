from fastapi import APIRouter, Depends, HTTPException
from app.services.loan_service import LoanService
from app.schemas.loan import LoanCreate, LoanRead, LoanReturn
from app.schemas.common import PaginatedResponse
from app.data.models import LoanStatus

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=LoanRead, status_code=201)
async def create_loan(
    loan: LoanCreate, service: LoanService = Depends()
):
    """
    Create a new loan.

    - **loan**: Loan data to create
    """
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
    service: LoanService = Depends(),
):
    """
    Retrieve a paginated list of loans with optional filtering.

    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20)
    - **status**: Filter by loan status
    - **borrower_mail**: Filter by borrower's email
    - **book_id**: Filter by book ID
    - **active_only**: Show only active loans
    - **late_only**: Show only late loans
    """
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
async def get_loan(loan_id: int, service: LoanService = Depends()):
    """
    Retrieve loan details by ID.

    - **loan_id**: The ID of the loan to retrieve
    """
    return await service.get_loan_details(loan_id)


@router.post("/{loan_id}/return", response_model=LoanRead)
async def return_loan(
    loan_id: int,
    return_data: LoanReturn,
    service: LoanService = Depends(),
):
    """
    Return a loan.

    - **loan_id**: The ID of the loan to return
    - **return_data**: Return data
    """
    return await service.return_loan(loan_id, return_data)


@router.post("/{loan_id}/renew", response_model=LoanRead)
async def renew_loan(loan_id: int, service: LoanService = Depends()):
    """
    Renew a loan.

    - **loan_id**: The ID of the loan to renew
    """
    return await service.renew_loan(loan_id)
