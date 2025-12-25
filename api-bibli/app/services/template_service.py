from typing import TypeVar, Generic, Type, List, Optional, Any
from sqlalchemy.future import select
from sqlalchemy import delete

from data.orm import SessionDep

T = TypeVar("T")


class TemplateService(Generic[T]):
    def __init__(self, session: SessionDep, model: Type[T]):
        self.session = session
        self.model = model

    async def get_all(self) -> List[T]:
        """
        Retrieve all entities of the model.
        """
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, id: Any) -> Optional[T]:
        """
        Retrieve an entity by its ID.

        - **id**: The ID of the entity to retrieve
        """
        result = await self.session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def add(self, entity: T) -> T:
        """
        Add a new entity to the database.

        - **entity**: The entity to add
        """
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def delete(self, id: Any) -> None:
        """
        Delete an entity by its ID.

        - **id**: The ID of the entity to delete
        """
        await self.session.execute(delete(self.model).where(self.model.id == id))
        await self.session.commit()

    async def update(self, entity: T) -> T:
        """
        Update an existing entity in the database.

        - **entity**: The entity to update
        """
        merged_entity = await self.session.merge(entity)
        await self.session.commit()
        return merged_entity
