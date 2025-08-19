import pytest
import pytest_asyncio
from src.api.schema.todo import ToDoCreate, ToDoFromDB
from src.api.schema.todo import StatusEnum
from aiohttp import ClientSession



@pytest_asyncio.fixture(scope='session')
async def single_task_id():
    async with ClientSession() as session:
        async with session.post('http://todo_service:8000/api/v1/create', json=(get_task_data())) as response:
            assert response.status == 201
            created_task = ToDoFromDB.model_validate((await response.json()).get('data'))
            
            yield created_task.id


def get_task_data(index: int = 0) -> dict:
    return ToDoCreate(
        title=f'Название {index}',
        description=f'Описание {index}'
    ).model_dump()


@pytest.mark.asyncio
async def test_create_multiple_tasks(async_client: ClientSession):
    '''
    Тест создания нескольких задач
    '''
    for i in range(3):
        task_data = get_task_data(i)
        response = await async_client.post('http://todo_service:8000/api/v1/create', json=task_data)
        assert response.status == 201


@pytest.mark.asyncio
async def test_get_all_tasks_by_status(async_client: ClientSession):
    '''
    Тест получения всех тасок со статусом TODO
    '''
    response = await async_client.get('http://todo_service:8000/api/v1/get_list_by_status?status=TODO')
    assert response.status == 200
    assert len((await response.json()).get('data')) == 3


@pytest.mark.asyncio
async def test_get_all_tasks(async_client: ClientSession):
    '''
    Тест получения всех тасок
    '''
    response = await async_client.get('http://todo_service:8000/api/v1/get_list')
    assert response.status == 200
    assert len((await response.json()).get('data')) == 3


@pytest.mark.asyncio
async def test_get_task_by_id(async_client: ClientSession, single_task_id):
    '''
    Тест получения таски по id
    '''
    print(single_task_id)
    response = await async_client.get(f'http://todo_service:8000/api/v1/get/{single_task_id}')
    assert response.status == 200
    task: ToDoFromDB = (ToDoFromDB.model_validate((await response.json()).get('data')))
    
    assert task.id == single_task_id


@pytest.mark.asyncio
async def test_update_task_status_by_id(async_client: ClientSession, single_task_id):
    '''
    Тест обновления статуса таски по id
    '''
    response = await async_client.put(f'http://todo_service:8000/api/v1/update/{single_task_id}?status=IN_PROGRESS')
    assert response.status == 200
    task = (ToDoFromDB.model_validate((await response.json()).get('data')))
    
    assert task.status == StatusEnum.IN_PROGRESS


@pytest.mark.asyncio
async def test_delete_task_by_id(async_client: ClientSession, single_task_id):
    '''
    Тест удаления таски по id
    '''
    response = await async_client.delete(f'http://todo_service:8000/api/v1/delete/{single_task_id}')
    assert response.status == 200

    response = await async_client.get('http://todo_service:8000/api/v1/get_list')
    assert len((await response.json()).get('data')) == 3


@pytest.mark.asyncio
async def test_delete_all_tasks(async_client: ClientSession):
    all_tasks = await async_client.get('http://todo_service:8000/api/v1/get_list')
    assert all_tasks.status == 200

    all_tasks = [i.get('id') for i in (await all_tasks.json()).get('data')]
    assert len(all_tasks) > 0

    for task in all_tasks:
        delete_response = await async_client.delete(f'http://todo_service:8000/api/v1/delete/{task}')
        assert delete_response.status == 200

    all_tasks = await async_client.get('http://todo_service:8000/api/v1/get_list')
    assert all_tasks.status == 200

    all_tasks = (await all_tasks.json()).get('data')
    assert len(all_tasks) == 0

