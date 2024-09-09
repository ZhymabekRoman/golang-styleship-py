from typing import Any, Callable, Coroutine, TypeVar, Union, Awaitable, Tuple
from dataclasses import dataclass
import sys
import asyncio
import inspect
import logging
import traceback

T = TypeVar("T")
R = TypeVar("R")

logger = logging.getLogger(__name__)


@dataclass
class ErrorInfo:
    exception: Exception
    traceback: str


def wrap_function(
    func: Union[Callable[..., T], Callable[..., Awaitable[T]]]
) -> Callable[
    ...,
    Union[
        Tuple[T | None, ErrorInfo | None], Awaitable[Tuple[T | None, ErrorInfo | None]]
    ],
]:
    async def async_wrapper(*args, **kwargs) -> Tuple[T | None, ErrorInfo | None]:
        try:
            result = await func(*args, **kwargs)  # type: ignore
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

    def sync_wrapper(*args, **kwargs) -> Tuple[T | None, ErrorInfo | None]:
        try:
            result = func(*args, **kwargs)  # type: ignore
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

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


def go_style_func(
    func: Union[Callable[..., T], Callable[..., Awaitable[T]]],
) -> Callable[..., Tuple[T | None, ErrorInfo | None]]:
    wrapper = wrap_function(func)

    def executor(*args: Any, **kwargs: Any) -> Tuple[T | None, ErrorInfo | None]:
        if asyncio.iscoroutinefunction(func):
            return asyncio.run(wrapper(*args, **kwargs))  # type: ignore
        return wrapper(*args, **kwargs)  # type: ignore

    return executor


gst = go_style_func


def go_style_func_async(
    func: Union[Callable[..., T], Callable[..., Awaitable[T]]]
) -> Callable[..., Coroutine[Any, Any, Tuple[T | None, ErrorInfo | None]]]:
    wrapper = wrap_function(func)

    async def executor(*args: Any, **kwargs: Any) -> Tuple[T | None, ErrorInfo | None]:
        if asyncio.iscoroutinefunction(func):
            return await wrapper(*args, **kwargs)  # type: ignore

        return await asyncio.to_thread(wrapper, *args, **kwargs)  # type: ignore

    return executor


def go_style_decorator(
    func: Union[Callable[..., T], Callable[..., Awaitable[T]]]
) -> Callable[
    ...,
    Union[
        Tuple[T | None, ErrorInfo | None], Awaitable[Tuple[T | None, ErrorInfo | None]]
    ],
]:
    return wrap_function(func)


gst = go_style_func
gsta = go_style_func_async
gstdec = go_style_decorator
