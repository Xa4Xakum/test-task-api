from typing import List
import sys
import traceback
from datetime import datetime
import functools

from loguru import logger


def error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            stack_trace = traceback.format_exc()
            caller_info = traceback.extract_stack(limit=3)[0]
            error_origin = traceback.extract_stack(limit=3)[-2]

            logger.error(
                f"Ошибка: {repr(e)}\n"
                f"Ошибка в функции '{func.__name__}' "
                f"(файл: {caller_info.filename}, строка: {caller_info.lineno})\n"
                f"Функция вызвана из '{error_origin.name}' "
                f"(файл: {error_origin.filename}, строка: {error_origin.lineno})\n"
                f"Аргументы: {args}, {kwargs}\n"
                f"Трассировка стека:\n{stack_trace}"
            )

            return f"При выполнении функции {func.__name__} в {error_time} произошла ошибка: {str(e)}"

    return wrapper


def is_int(string: str | List[str]) -> bool:
    '''
    Проверяет, является ли строка числом

    :param string: Проверяемая строка или список проверяемых строк
    '''
    try:
        if isinstance(string, list):
            for i in string:
                int(i)
        else:
            int(string)
        return True
    except Exception:
        return False


def is_float(string: str | List[str]) -> bool:
    '''
    Проверяет, является ли строка числом

    :param string: Проверяемая строка или список проверяемых строк
    '''
    try:
        if isinstance(string, list):
            for i in string:
                float(i)
        else:
            float(string)
        return True
    except Exception:
        return False


def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG",
        colorize=True
    )

    logger.add(
        "logs/err_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="1 day",
        retention="7 days",
        compression="zip"
    )

    logger.add(
        "logs/log_{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="00:00",
        retention="3 days",
    )
