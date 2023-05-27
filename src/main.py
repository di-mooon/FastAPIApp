import logging

import asyncpg
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.common.utils import init_logging
from src.database import init_models
from src.questions.router import question_router
from src.records.router import record_router
from src.users.router import user_router

app = FastAPI()
app.include_router(question_router)
app.include_router(user_router)
app.include_router(record_router)
logger = logging.getLogger()


@app.on_event("startup")
async def on_startup():
    init_logging()
    await init_models()


@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(exc)
    return JSONResponse(
        content={"error": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.exception_handler(asyncpg.exceptions.PostgresError)
async def pg_exception_handler(request: Request, exc: asyncpg.exceptions.PostgresError):
    logger.error(exc)
    return JSONResponse(
        content={"error": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
