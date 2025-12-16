from pydantic import BaseModel
import datetime

class Author(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    date_of_death: datetime.date | None = None
    nationality: str
    biography: str | None = None
    website: str | None = None