from pydantic import BaseModel, Field, field_validator, model_validator
import datetime


# Author model
class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: datetime.date
    date_of_death: datetime.date | None = None
    nationality: str = Field(
        ..., min_length=2, max_length=3, description="ISO country code"
    )
    biography: str | None = None
    website: str | None = None

    @model_validator(mode="after")
    def check_dates(self):
        if self.date_of_death and self.date_of_death < self.date_of_birth:
            raise ValueError("Date of death must be after date of birth")
        return self


class AuthorRead(AuthorBase):
    id: int


class AuthorUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: datetime.date | None = None
    date_of_death: datetime.date | None = None
    nationality: str | None = None
    biography: str | None = None
    website: str | None = None

    @field_validator("nationality")
    def validate_nationality(cls, value):
        if value is not None and (len(value) < 2 or len(value) > 3):
            raise ValueError("ISO country code must be between 2 and 3 characters")
        return value

    @model_validator(mode="after")
    def check_dates(self):
        if self.date_of_birth and self.date_of_death:
            if self.date_of_death < self.date_of_birth:
                raise ValueError("Date of death must be after date of birth")
        return self
