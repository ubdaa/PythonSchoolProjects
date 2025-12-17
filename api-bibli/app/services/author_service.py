from sqlalchemy import select
from services.template_service import TemplateService
from data.orm import Author, SessionDep

class AuthorService(TemplateService[Author]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Author)
        
    async def get_by_fullname(self, first_name: str, last_name: str):
        statement = select(self.model).where(
            self.model.first_name == first_name,
            self.model.last_name == last_name
        )
        result = await self.session.execute(statement)
        return result.first()