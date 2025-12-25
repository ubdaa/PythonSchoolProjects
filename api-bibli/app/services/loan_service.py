from datetime import datetime, timedelta
from sqlalchemy import select, func, or_
from fastapi import HTTPException
from app.services.template_service import TemplateService
from app.data.orm import Loan, Book, SessionDep
from app.data.models import LoanStatus
from app.schemas.loan import LoanCreate, LoanReturn

# Configuration constants
MAX_LOANS_PER_USER = 5
LOAN_DURATION_DAYS = 14
PENALTY_RATE_PER_DAY = 0.5
MAX_PENALTY = 10.0


class LoanService(TemplateService[Loan]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Loan)

    def _calculate_penalty(
        self, due_date: datetime, return_date: datetime
    ) -> tuple[float, int]:
        if return_date <= due_date:
            return 0.0, 0

        days_late = (return_date - due_date).days
        penalty = min(days_late * PENALTY_RATE_PER_DAY, MAX_PENALTY)
        return round(penalty, 2), days_late

    def _enrich_loan(self, loan: Loan, book_title: str | None = None):
        """Helper to attach computed fields to the ORM object for the schema"""
        # Update status based on time if active
        if not loan.return_date and datetime.now() > loan.due_date:
            loan.status = LoanStatus.OVERDUE

        penalty = 0.0
        days_late = 0

        calc_date = loan.return_date if loan.return_date else datetime.now()
        if loan.status == LoanStatus.OVERDUE or (
            loan.return_date and loan.return_date > loan.due_date
        ):
            penalty, days_late = self._calculate_penalty(loan.due_date, calc_date)

        # Attach attributes dynamically so Pydantic can pick them up
        setattr(loan, "penalty", penalty)
        setattr(loan, "days_late", days_late)
        if book_title:
            setattr(loan, "book_title", book_title)
        elif loan.book:
            setattr(loan, "book_title", loan.book.title)

        return loan

    async def create_loan(self, loan_data: LoanCreate) -> Loan:
        """
        Create a new loan.

        - **loan_data**: The loan data to create
        """
        # 1. Check book existence
        book_stmt = select(Book).where(Book.id == loan_data.book_id)
        result = await self.session.execute(book_stmt)
        book = result.scalar_one_or_none()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        # 2. Check availability
        if book.available_copies <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"Book '{book.title}' is not currently available",
            )

        # 3. Check user loan limit
        count_stmt = select(func.count()).where(
            Loan.borrower_mail == loan_data.borrower_mail,
            or_(Loan.status == LoanStatus.ON_LOAN, Loan.status == LoanStatus.OVERDUE),
        )
        count_res = await self.session.execute(count_stmt)
        active_loans = count_res.scalar_one()

        if active_loans >= MAX_LOANS_PER_USER:
            raise HTTPException(
                status_code=400, detail=f"Loan limit reached ({MAX_LOANS_PER_USER} max)"
            )

        # 4. Create loan
        now = datetime.now()
        due_date = now + timedelta(days=LOAN_DURATION_DAYS)

        db_loan = Loan(
            **loan_data.model_dump(),
            loan_date=now,
            due_date=due_date,
            status=LoanStatus.ON_LOAN,
        )

        # 5. Update book copies
        book.available_copies -= 1

        self.session.add(db_loan)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(db_loan)

        # Eager load book for response
        await self.session.refresh(db_loan, attribute_names=["book"])
        return self._enrich_loan(db_loan)

    async def get_all_filtered(
        self,
        page: int,
        page_size: int,
        status: LoanStatus | None = None,
        borrower_mail: str | None = None,
        book_id: int | None = None,
        active_only: bool = False,
        late_only: bool = False,
    ):
        """
        Retrieve a paginated list of loans with optional filtering.

        - **page**: Page number
        - **page_size**: Number of items per page
        - **status**: Filter by loan status
        - **borrower_mail**: Filter by borrower's email
        - **book_id**: Filter by book ID
        - **active_only**: Show only active loans
        - **late_only**: Show only late loans
        """
        statement = select(Loan).join(Book)

        if status:
            statement = statement.where(Loan.status == status)
        if borrower_mail:
            statement = statement.where(Loan.borrower_mail.ilike(f"%{borrower_mail}%"))
        if book_id:
            statement = statement.where(Loan.book_id == book_id)
        if active_only:
            statement = statement.where(
                or_(
                    Loan.status == LoanStatus.ON_LOAN, Loan.status == LoanStatus.OVERDUE
                )
            )
        if late_only:
            statement = statement.where(Loan.status == LoanStatus.OVERDUE)

        statement = statement.order_by(Loan.loan_date.desc())

        # Count total
        total_stmt = select(func.count()).select_from(statement.subquery())
        total_res = await self.session.execute(total_stmt)
        total = total_res.scalar_one()

        # Pagination
        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)

        result = await self.session.execute(statement)
        loans = result.scalars().all()

        # Enrich with details
        enriched_loans = [self._enrich_loan(loan) for loan in loans]

        # Commit any status updates (e.g. changing ON_LOAN to OVERDUE during enrichment)
        if enriched_loans:
            await self.session.commit()

        return enriched_loans, total

    async def get_loan_details(self, loan_id: int) -> Loan:
        """
        Retrieve loan details by ID.

        - **loan_id**: The ID of the loan to retrieve
        """
        stmt = select(Loan).where(Loan.id == loan_id)
        result = await self.session.execute(stmt)
        loan = result.scalar_one_or_none()

        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        await self.session.refresh(loan, attribute_names=["book"])
        loan = self._enrich_loan(loan)
        await self.session.commit()  # Save status updates if any
        return loan

    async def return_loan(self, loan_id: int, return_data: LoanReturn) -> Loan:
        """
        Return a loan.

        - **loan_id**: The ID of the loan to return
        - **return_data**: Return data
        """
        loan = await self.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        if loan.return_date:
            raise HTTPException(status_code=400, detail="Loan already returned")

        # Get book
        book_stmt = select(Book).where(Book.id == loan.book_id)
        res = await self.session.execute(book_stmt)
        book = res.scalar_one()

        # Update loan
        return_date = return_data.return_date or datetime.now()
        loan.return_date = return_date
        loan.status = LoanStatus.RETURNED
        if return_data.comments:
            loan.comments = (
                f"{loan.comments}\n{return_data.comments}"
                if loan.comments
                else return_data.comments
            )

        # Update book
        book.available_copies += 1

        self.session.add(loan)
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(loan, attribute_names=["book"])

        return self._enrich_loan(loan)

    async def renew_loan(self, loan_id: int) -> Loan:
        """
        Renew a loan.

        - **loan_id**: The ID of the loan to renew
        """
        loan = await self.get_by_id(loan_id)
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        if loan.return_date:
            raise HTTPException(status_code=400, detail="Cannot renew a returned loan")

        if loan.renewed:
            raise HTTPException(status_code=400, detail="Loan already renewed once")

        loan.due_date += timedelta(days=LOAN_DURATION_DAYS)
        loan.renewed = True

        # Re-evaluate status (might no longer be overdue)
        if loan.status == LoanStatus.OVERDUE and datetime.now() <= loan.due_date:
            loan.status = LoanStatus.ON_LOAN

        self.session.add(loan)
        await self.session.commit()
        await self.session.refresh(loan, attribute_names=["book"])

        return self._enrich_loan(loan)
