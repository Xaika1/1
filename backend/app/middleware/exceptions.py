from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger("exceptions")

async def validation_handler(request: Request, exc: RequestValidationError):
    logger.warning("Ошибка валидации: %s", str(exc))
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": "Неверные данные запроса", "errors": exc.errors()})

async def integrity_handler(request: Request, exc: IntegrityError):
    logger.error("Конфликт целостности: %s", str(exc))
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "Нарушение целостности базы данных"})

async def generic_handler(request: Request, exc: Exception):
    logger.exception("Необработанная ошибка: %s", str(exc))
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Внутренняя ошибка сервера"})

def register_handlers(app):
    app.add_exception_handler(RequestValidationError, validation_handler)
    app.add_exception_handler(IntegrityError, integrity_handler)
    app.add_exception_handler(Exception, generic_handler)