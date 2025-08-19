from database.repos.base_repo import Repository
from database.model import Tasks
from sqlalchemy import select, delete, update


class TaskRepository(Repository):
    model = Tasks

    async def get_all_by_status(self, status: str | None):
        return (
            (
                await self.session.execute(
                    select(self.model).filter(self.model.status == status)
                )
            )
            .scalars()
            .all()
        )

    async def update_status_by_id(self, id: str, status: str):
        result = await self.session.execute(
            update(self.model)
            .values(status=status)
            .where(self.model.id == id)
            .returning(self.model)
        )
        return result.scalar_one_or_none()

    async def delete_by_id(self, id: str):
        await self.session.execute(delete(self.model).where(self.model.id == id))
