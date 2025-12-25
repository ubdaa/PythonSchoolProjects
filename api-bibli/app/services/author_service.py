from sqlalchemy import func, select
from app.services.template_service import TemplateService
from app.data.orm import Author, SessionDep


class AuthorService(TemplateService[Author]):
    def __init__(self, session: SessionDep):
        super().__init__(self, Author)

    async def get_by_fullname(self, first_name: str, last_name: str):
        """
        Retrieve an author by full name.

        - **first_name**: The first name of the author
        - **last_name**: The last name of the author
        """
        statement = select(self.model).where(
            self.model.first_name == first_name, self.model.last_name == last_name
        )
        result = await self.session.execute(statement)
        return result.first()

    async def get_all_filtered(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        nationality: str | None = None,
        sort_by: str = "last_name",
        order: str = "asc",
    ):
        """
        Retrieve a paginated list of authors with optional filtering.

        - **page**: Page number
        - **page_size**: Number of items per page
        - **search**: Search term for name or biography
        - **nationality**: Filter by nationality
        - **sort_by**: Sort field
        - **order**: Sort order (asc or desc)
        """
        statement = select(self.model)
        if search:
            statement = statement.where(
                (self.model.first_name.ilike(f"%{search}%"))
                | (self.model.last_name.ilike(f"%{search}%"))
                | (self.model.biography.ilike(f"%{search}%"))
                | (self.model.website.ilike(f"%{search}%"))
            )

        if nationality:
            statement = statement.where(self.model.nationality == nationality.upper())

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
