from utils.unitofwork import IUnitOfWork
from api.schema.todo import ToDoCreate, ToDoFromDB


class ToDoService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def add_todo(self, todo: ToDoCreate) -> ToDoFromDB:
        '''
        Добавление задачи
        Args:
            todo (ToDoCreate): Задача к добавлению 
        '''
        todo_dict: dict = todo.model_dump()
        async with self.uow:
            todo_from_db = await self.uow.todo.add_one(todo_dict)
            todo_to_return = ToDoFromDB.model_validate(todo_from_db)
            await self.uow.commit()
            return todo_to_return

    async def get_tasks(self) -> list[ToDoFromDB]:
        '''
        Получение задач списком
        '''
        async with self.uow:
            todos = await self.uow.todo.get_all()
            return [ToDoFromDB.model_validate(todo) for todo in todos]

    async def get_tasks_by_status(self, status: str) -> list[ToDoFromDB]:
        '''
        Получение задач по статусу
            status (str): Статус, по которому искать задачи
        '''
        async with self.uow:
            todos = await self.uow.todo.get_all_by_status(status)
            return [ToDoFromDB.model_validate(todo) for todo in todos]

    async def get_task(self, id: str) -> ToDoFromDB | None:
        '''
        Получение задачи по ID
        Args:
            id (str): UUID задачи в строковом формате
        '''
        async with self.uow:
            todo = await self.uow.todo.get_by_id(id)
            if todo:
                return ToDoFromDB.model_validate(todo)
            return None

    async def update_status_by_id(self, id: str, status: str) -> ToDoFromDB:
        '''
        Обновление статуса задачи по ID
        Args:
            id (str): UUID задачи в строковом формате
            status (str): Новый статус задачи
        '''
        async with self.uow:
            todo = await self.uow.todo.update_status_by_id(id, status)
            if not todo:
                return None
            todo_return = ToDoFromDB.model_validate(todo)
            await self.uow.commit()
            return todo_return

    async def delete_by_id(self, id: str):
        '''
        Удаление задачи по ID
        Args:
            id (str): UUID задачи в строковом формате
        '''
        async with self.uow:
            await self.uow.todo.delete_by_id(id)
            await self.uow.commit()
