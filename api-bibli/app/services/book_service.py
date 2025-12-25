from sqlalchemy import func, select
from services.template_service import TemplateService
from data.orm import Book, SessionDep


class BookService(TemplateService[Book]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Book)

    async def get_by_isbn(self, isbn: str):
        statement = select(self.model).where(self.model.isbn == isbn)
        result = await self.session.execute(statement)
        return result.first()

    async def get_all_filtered(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        isbn: str | None = None,
        category: str | None = None,
        language: str | None = None,
        sort_by: str = "title",
        order: str = "asc",
    ):
        statement = select(self.model)
        if search:
            statement = statement.where(
                (self.model.title.ilike(f"%{search}%"))
                | (self.model.description.ilike(f"%{search}%"))
            )

        if isbn:
            statement = statement.where((self.model.isbn.ilike(f"%{isbn}%")))

        if category:
            statement = statement.where(self.model.category == category)

        if language:
            statement = statement.where(self.model.language == language)

        sort_column = getattr(self.model, sort_by)
        if order == "desc":
            statement = statement.order_by(sort_column.desc())
        else:
            statement = statement.order_by(sort_column)

        total_statement = select(func.count()).select_from(statement.subquery())
        total_result = await self.session.execute(total_statement)
        total = total_result.scalar_one()
        offset = (page - 1) * page_size
        statement = statement.offset(offset).limit(page_size)
        result = await self.session.execute(statement)
        items = result.scalars().all()
        return items, total
