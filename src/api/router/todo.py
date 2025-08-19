from fastapi import Depends
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from service.todo_service import ToDoService
from api.dependencies import get_todo_service
from api.schema.todo import ToDoCreate, StatusEnum, BaseResponse


router = APIRouter()


@router.post("/create",
            summary="Создание таски",
            response_model=BaseResponse,
            status_code=201,
            responses={
                201: {'description': 'Таска успешно создана'},
                409: {'description': 'Таска уже существует'},
                500: {'description': 'Произошла ошибка в создании таски'} 
            }
        )
async def create_task(
    todo: ToDoCreate, todo_service: ToDoService = Depends(get_todo_service)
):
    if todo in await todo_service.get_tasks():
        raise HTTPException(409, detail="Task already exists!")
    
    created_task = await todo_service.add_todo(todo)
    
    return BaseResponse(
        status='success',
        data=created_task.model_dump()
    )

@router.get("/get_list_by_status",
            summary="Получение всех таск с фильтрацией по статусу",
            response_model=BaseResponse,
            responses={
                200: {'description': 'Все таски cо сатусом n получены'},
                500: {'description': 'Произошла ошибка в получении тасок'} 
            }
        )
async def get_tasks(
    status: StatusEnum | None = None,
    todo_service: ToDoService = Depends(get_todo_service),
):
    tasks = await todo_service.get_tasks_by_status(status)
    return BaseResponse(
        status='success',
        data=tasks
    )

@router.get("/get_list",
            summary="Получение всех тасок",
            response_model=BaseResponse,
            responses={
                200: {'description': 'Все таски получены'},
                500: {'description': 'Произошла ошибка в получении тасок'} 
            }
        )
async def get_tasks(
    todo_service: ToDoService = Depends(get_todo_service),
):
    tasks = await todo_service.get_tasks()
    return BaseResponse(
        status='success',
        data=tasks
    )


@router.get("/get/{todo_id}",
            summary="Получение таска по id",
            response_model=BaseResponse,
            responses={
                200: {'description': 'Таск получен'},
                404: {'description': 'Таск не найден'},
                500: {'description': 'Произошла ошибка в получении таски'} 
            }
        )
async def get_task_by_id(
    todo_id: str, todo_service: ToDoService = Depends(get_todo_service)
):
    task = await todo_service.get_task(todo_id)
    if not task:
        raise HTTPException(404, "Task not found")

    return BaseResponse(
        status='success',
        data=task.model_dump()
    )


@router.put("/update/{task_id}",
            summary="Обновление статуса таски по id",
            response_model=BaseResponse,
            responses={
                200: {'description': 'Статус успешно обновлен'},
                500: {'description': 'Произошла ошибка в обновлении статуса'} 
            }
        )
async def update_task_by_id(
    task_id: str,
    status: StatusEnum,
    todo_service: ToDoService = Depends(get_todo_service),
):
    task = await todo_service.update_status_by_id(task_id, status)
    
    if not task:
        raise HTTPException(404, 'Task to update not found')
    
    return BaseResponse(
        status='success',
        data=task.model_dump()
    )


@router.delete("/delete/{task_id}",
                summary="Удаление таски по id",
                responses={
                    200: {'description': 'Таска успешно удалена'},
                    500: {'description': 'Произошла ошибка удалении таски'} 
                }
            )
async def delete_task_by_id(
    task_id: str, todo_service: ToDoService = Depends(get_todo_service)
):
    await todo_service.delete_by_id(task_id)
