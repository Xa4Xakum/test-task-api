from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from loguru import logger


async def exception_middleware(request: Request, call_next):
    try:
        err = None
        response = await call_next(request)
        return response

    except ValidationError as e: err = Error(422, e.errors())
    except HTTPException as e: err = Error(e.status_code, e.detail)

    except Exception as e:
        logger.opt(exception=True).error(f"🔴 Ошибка при обработке сообщения от {request.client.host if request.client else 'неизвестный клиент'}")
        err = Error(500, f"Internal server error")

    finally:
        if err:
            return JSONResponse(status_code=err.code, content=err.api_answer())


class Error():
    '''Ошибка при выполнении'''

    def __init__(self, code: int, err: str):
        self.code = code
        self.err = err

    def api_answer(self) -> dict:
        return {
            'detail': self.err
        }