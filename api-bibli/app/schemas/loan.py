from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from data.models import LoanStatus

class LoanBase(BaseModel):
    borrower_name: str
    borrower_mail: EmailStr
    card_number: str
    comments: str | None = None

class LoanCreate(LoanBase):
    book_id: int

class LoanReturn(BaseModel):
    return_date: datetime | None = None
    comments: str | None = None

class LoanRead(LoanBase):
    id: int
    book_id: int
    loan_date: datetime
    due_date: datetime
    return_date: datetime | None = None
    status: LoanStatus
    renewed: bool
    book_title: str | None = None
    penalty: float = 0.0
    days_late: int = 0

    class Config:
        from_attributes = True
