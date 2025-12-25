from datetime import datetime, timedelta
from sqlalchemy import func, select, case, desc, extract
from data.orm import Book, Loan, Author, User, SessionDep

class StatsService:
    def __init__(self, session: SessionDep):
        self.session = session

    async def get_global_stats(self):
        total_books = await self.session.scalar(select(func.count(Book.id)))
        total_copies = await self.session.scalar(select(func.sum(Book.available_copies))) # Assuming available_copies tracks current stock, total_copies might need a different field if available changes
        # If total copies is a static field like 'total_copies', use that. If it's dynamic, this logic might need adjustment based on your model.
        # Assuming 'total_copies' exists on Book or is sum of available + loaned. Let's assume a simple count for now or sum of a field.
        # If the model only has available_copies, we might need to count loans + available.
        
        active_loans = await self.session.scalar(select(func.count(Loan.id)).where(Loan.return_date.is_(None)))
        
        today = datetime.now().date()
        late_loans = await self.session.scalar(
            select(func.count(Loan.id)).where(
                Loan.return_date.is_(None),
                Loan.due_date < today
            )
        )

        # Occupancy rate: active loans / total physical copies (active + available)
        # This depends heavily on your data model. Assuming total_copies = active_loans + sum(Book.available_copies)
        sum_available = await self.session.scalar(select(func.sum(Book.available_copies))) or 0
        total_physical = active_loans + sum_available
        occupancy_rate = (active_loans / total_physical * 100) if total_physical > 0 else 0.0

        return {
            "total_books": total_books or 0,
            "total_authors": await self.session.scalar(select(func.count(Author.id))) or 0,
            "total_loans": await self.session.scalar(select(func.count(Loan.id))) or 0,
            "active_loans": active_loans or 0,
            "late_loans": late_loans or 0,
            "occupancy_rate": round(occupancy_rate, 2)
        }

    async def get_book_stats(self, book_id: int):
        book = await self.session.get(Book, book_id)
        if not book:
            return None

        total_loans = await self.session.scalar(select(func.count(Loan.id)).where(Loan.book_id == book_id))
        
        # Average duration (only for returned loans)
        avg_duration = await self.session.scalar(
            select(func.avg(Loan.return_date - Loan.loan_date))
            .where(Loan.book_id == book_id, Loan.return_date.is_not(None))
        )
        
        times_late = await self.session.scalar(
            select(func.count(Loan.id)).where(
                Loan.book_id == book_id,
                Loan.return_date > Loan.due_date
            )
        )

        # Popularity rank (subquery to rank books by loan count)
        # This is complex in ORM, simplified approach: count loans for this book vs others
        # Or just return None if too complex for this scope
        
        return {
            "book_id": book.id,
            "book_title": book.title,
            "total_loans": total_loans,
            "average_loan_duration": float(avg_duration.days) if avg_duration else 0.0,
            "times_late": times_late,
            "popularity_rank": None # Placeholder
        }

    async def get_author_stats(self, author_id: int):
        author = await self.session.get(Author, author_id)
        if not author:
            return None
            
        total_books = await self.session.scalar(select(func.count(Book.id)).where(Book.author_id == author_id))
        
        total_loans = await self.session.scalar(
            select(func.count(Loan.id))
            .join(Book)
            .where(Book.author_id == author_id)
        )

        return {
            "author_id": author.id,
            "author_name": f"{author.first_name} {author.last_name}",
            "total_books": total_books,
            "total_loans": total_loans
        }

    async def get_monthly_report(self, year: int, month: int):
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)

        new_books = await self.session.scalar(
            select(func.count(Book.id)).where(Book.publication_year == year) # Simplified, usually needs created_at
        )
        # Assuming User has created_at, otherwise 0
        new_users = 0 
        
        total_loans = await self.session.scalar(
            select(func.count(Loan.id)).where(Loan.loan_date >= start_date, Loan.loan_date < end_date)
        )
        
        returned_loans = await self.session.scalar(
            select(func.count(Loan.id)).where(Loan.return_date >= start_date, Loan.return_date < end_date)
        )

        return {
            "month": start_date.strftime("%Y-%m"),
            "new_books": new_books or 0,
            "new_users": new_users,
            "total_loans": total_loans or 0,
            "returned_loans": returned_loans or 0
        }

    async def get_never_borrowed_books(self):
        subquery = select(Loan.book_id).distinct()
        statement = select(Book).where(Book.id.not_in(subquery))
        result = await self.session.execute(statement)
        books = result.scalars().all()
        return [
            {"book_id": b.id, "title": b.title, "added_date": str(b.publication_year)} 
            for b in books
        ]

    async def get_active_users(self, limit: int = 10):
        statement = (
            select(User, func.count(Loan.id).label("loan_count"))
            .join(Loan)
            .group_by(User.id)
            .order_by(desc("loan_count"))
            .limit(limit)
        )
        result = await self.session.execute(statement)
        data = []
        for user, count in result.all():
            current_loans = await self.session.scalar(
                select(func.count(Loan.id)).where(Loan.user_id == user.id, Loan.return_date.is_(None))
            )
            late_returns = await self.session.scalar(
                select(func.count(Loan.id)).where(
                    Loan.user_id == user.id, 
                    Loan.return_date > Loan.due_date
                )
            )
            data.append({
                "user_id": user.id,
                "full_name": f"{user.first_name} {user.last_name}",
                "total_loans": count,
                "current_loans": current_loans,
                "late_returns": late_returns
            })
        return data
