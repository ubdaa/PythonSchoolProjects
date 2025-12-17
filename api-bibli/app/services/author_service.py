from services.template_service import TemplateService
from data.models import Author
from data.orm import SessionDep

class AuthorService(TemplateService[Author]):
    def __init__(self, session: SessionDep):
        super().__init__(session, Author)