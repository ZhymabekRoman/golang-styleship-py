from _typeshed import Incomplete
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, TypeVar

T = TypeVar('T')
logger: Incomplete

@dataclass
class ErrorInfo:
    exception: BaseException
    traceback: str
    def __init__(self, exception, traceback) -> None: ...

def wrap_sync_function(func: Callable[..., T]) -> Callable[..., tuple[T | None, ErrorInfo | None]]: ...
def wrap_async_function(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[tuple[T | None, ErrorInfo | None]]]: ...
def gst(func: Callable[..., T]) -> Callable[..., tuple[T | None, ErrorInfo | None]]: ...
def gsta(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[tuple[T | None, ErrorInfo | None]]]: ...
def gstdec(func: Callable[..., Any]) -> Callable[..., Any]: ...
go_style_func = gst
go_style_func_async = gsta
go_style_decorator = gstdec
