from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Book(SQLModel, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titre: str = Field(index=True)
    auteur: str
    isbn: str = Field(index=True, unique=True)
    annee_publication: int
    disponible: bool = Field(default=True)
    date_ajout: datetime = Field(default_factory=datetime.now)
    
class BookCreate(BaseModel):
    titre: str
    auteur: str
    isbn: str
    annee_publication: int
    disponible: bool = True
    
class BookRead(BaseModel):
    id: int

    class Config:
        from_attributes = True

class BookUpdate(BaseModel):
    titre: Optional[str] = None
    auteur: Optional[str] = None
    isbn: Optional[str] = None
    annee_publication: Optional[int] = None
    disponible: Optional[bool] = None