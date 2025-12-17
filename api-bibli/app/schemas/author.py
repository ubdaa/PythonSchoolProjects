from pydantic import BaseModel, Field, field_validator, EmailStr, model_validator
from enum import Enum
import datetime

# Author model
class Author(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    date_of_death: datetime.date | None = None
    nationality: str = Field(..., min_length=2, max_length=3, description="ISO country code")
    biography: str | None = None
    website: str | None = None

    @model_validator(mode='after')
    def check_dates(self):
        if self.date_of_death and self.date_of_death < self.date_of_birth:
            raise ValueError('Date of death must be after date of birth')
        return self
