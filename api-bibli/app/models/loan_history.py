from pydantic import BaseModel
import datetime

class LoanHistory(BaseModel):
    id: int
    book_id: int
    loan_number: int
    book_popularity: int