from fastapi import Depends
from service.todo_service import ToDoService
from utils.unitofwork import IUnitOfWork, UnitOfWork


async def get_todo_service(uow: IUnitOfWork = Depends(UnitOfWork)):
    return ToDoService(uow)
