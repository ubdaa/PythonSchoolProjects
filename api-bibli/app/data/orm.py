from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Float, Text, Enum as SqEnum
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from data.models import BookCategory, LoanStatus

DATABASE_URL = "sqlite+aiosqlite:///./library.db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    date_of_death = Column(Date, nullable=True)
    nationality = Column(String, nullable=False)
    biography = Column(Text, nullable=True)
    website = Column(String, nullable=True)

    # Relationships
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    year = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    available_copies = Column(Integer, default=0)
    total_copies_owned = Column(Integer, default=0)
    description = Column(Text, nullable=True)
    category = Column(SqEnum(BookCategory), nullable=False)
    language = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    publisher = Column(String, nullable=False)

    # Relationships
    author = relationship("Author", back_populates="books")
    loans = relationship("Loan", back_populates="book")
    history = relationship("LoanHistory", back_populates="book", uselist=False)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_name = Column(String, nullable=False)
    borrower_mail = Column(String, nullable=False)
    card_number = Column(String, nullable=False)
    loan_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(SqEnum(LoanStatus), default=LoanStatus.ON_LOAN)
    comments = Column(Text, nullable=True)

    # Relationships
    book = relationship("Book", back_populates="loans")


class LoanHistory(Base):
    __tablename__ = "loan_histories"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), unique=True, nullable=False)
    total_loans = Column(Integer, default=0)
    average_duration_days = Column(Float, default=0.0)
    popularity_score = Column(Integer, default=0)

    # Relationships
    book = relationship("Book", back_populates="history")


def init_db():
    """Creates the database tables."""
    Base.metadata.create_all(bind=engine)
    
    
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
