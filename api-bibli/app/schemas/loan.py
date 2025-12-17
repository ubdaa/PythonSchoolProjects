from pydantic import BaseModel, Field, field_validator, EmailStr, model_validator
from enum import Enum
import datetime 

# Loan models
class LoanStatus(str, Enum):
    ON_LOAN = "On Loan"
    RETURNED = "Returned"
    OVERDUE = "Overdue"

class Loan(BaseModel):
    book_id: int
    borrower_name: str
    borrower_mail: EmailStr
    card_number: str
    loan_date: datetime.datetime
    due_date: datetime.datetime
    return_date: datetime.datetime | None = None
    status: LoanStatus
    comments: str | None = None

    @model_validator(mode='after')
    def check_return_date(self):
        if self.return_date and self.return_date < self.loan_date:
            raise ValueError('Return date must be after loan date')
        return self
