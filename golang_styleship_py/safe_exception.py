import asyncio
import logging
import sys
import traceback
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Optional, Tuple, TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)


@dataclass
class ErrorInfo:
    exception: Exception
    traceback: str


def wrap_sync_function(
    func: Callable[..., T],
) -> Callable[..., Tuple[Optional[T], Optional[ErrorInfo]]]:
    def sync_wrapper(
        *args: Any, **kwargs: Any
    ) -> Tuple[Optional[T], Optional[ErrorInfo]]:
        try:
            result = func(*args, **kwargs)
            logger.info(f"Function {func.__name__} executed successfully")
            return result, None
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_str = "".join(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            )
            error_info = ErrorInfo(exception=e, traceback=tb_str)
            logger.error(f"Exception in {func.__name__}: {str(e)}\n{tb_str}")
            return None, error_info

    return sync_wrapper


def wrap_async_function(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[Tuple[Optional[T], Optional[ErrorInfo]]]]:
    async def async_wrapper(
        *args: Any, **kwargs: Any
    ) -> Tuple[Optional[T], Optional[ErrorInfo]]:
        try:
            result = await func(*args, **kwargs)
            logger.info(f"Function {func.__name__} executed successfully")
            return result, None
        except BaseException as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_str = "".join(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            )
            error_info = ErrorInfo(exception=e, traceback=tb_str)
            logger.error(f"Exception in {func.__name__}: {str(e)}\n{tb_str}")
            return None, error_info

    return async_wrapper


def gst(
    func: Callable[..., T],
) -> Callable[..., Tuple[Optional[T], Optional[ErrorInfo]]]:
    """
    Decorator for synchronous functions.
    """
    if asyncio.iscoroutinefunction(func):
        # If a coroutine function is mistakenly decorated with gst, raise an error.
        raise TypeError("gst decorator cannot be applied to asynchronous functions.")
    return wrap_sync_function(func)


def gsta(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[Tuple[Optional[T], Optional[ErrorInfo]]]]:
    """
    Decorator for asynchronous functions.
    """
    if not asyncio.iscoroutinefunction(func):
        # If a regular function is mistakenly decorated with gsta, raise an error.
        raise TypeError("gsta decorator can only be applied to asynchronous functions.")
    return wrap_async_function(func)


def gstdec(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    General decorator that wraps both synchronous and asynchronous functions.
    """
    if asyncio.iscoroutinefunction(func):
        return wrap_async_function(func)
    return wrap_sync_function(func)


# Remove redundant assignments
go_style_func = gst
go_style_func_async = gsta
go_style_decorator = gstdec
