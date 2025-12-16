from pydantic import BaseModel
import datetime

class LoanStatus(str):
    ON_LOAN = "On Loan"
    RETURNED = "Returned"
    OVERDUE = "Overdue"

class Loan(BaseModel):
    id: int
    book_id: int
    borrower_name: str
    borrower_mail: str
    card_number: str
    loan_date: datetime.date
    due_date: datetime.date
    return_date: datetime.date | None = None
    status: LoanStatus
    comments: str | None = None
    