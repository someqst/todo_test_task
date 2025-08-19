from fastapi import FastAPI
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator

from utils.logging import logger
from api.router.todo import router as todo_router


app = FastAPI(title="ToDo List")
(Instrumentator().instrument(app)).expose(app)


@app.exception_handler(Exception)
async def default_exception_handler(req: Request, exc: Exception):
    logger.error(exc)
    raise HTTPException(status_code=500, detail="Internal Server Error")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['127.0.0.1:8000', '127.0.0.1'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(todo_router, prefix="/api/v1", tags=["todo"])
