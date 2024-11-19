from typing import Optional

import pytest

from golang_styleship_py.safe_exception import ErrorInfo, gst, gsta


# Test helper functions
def sync_returns_int() -> int:
    return 42


async def async_returns_str() -> str:
    return "hello"


class CustomType:
    value: str

    def __init__(self, value: str):
        self.value = value


def sync_returns_custom() -> CustomType:
    return CustomType("test")


async def async_returns_optional() -> Optional[int]:
    return None


# Sync function tests
def test_sync_int_types():
    wrapped = gst(sync_returns_int)
    result, error = wrapped()
    assert isinstance(result, int)
    assert error is None


def test_sync_custom_types():
    wrapped = gst(sync_returns_custom)
    result, error = wrapped()
    assert isinstance(result, CustomType)
    assert error is None


# Async function tests
@pytest.mark.asyncio
async def test_async_str_types():
    wrapped = gsta(async_returns_str)
    result, error = await wrapped()
    assert isinstance(result, str)
    assert error is None


@pytest.mark.asyncio
async def test_async_optional_types():
    wrapped = gsta(async_returns_optional)
    result, error = await wrapped()
    assert result is None
    assert error is None


# Error case tests
def test_sync_error_types():
    def raises_error() -> int:
        raise ValueError("test error")

    wrapped = gst(raises_error)
    result, error = wrapped()
    assert result is None
    assert isinstance(error, ErrorInfo)
    assert isinstance(error.exception, ValueError)
    assert isinstance(error.traceback, str)


@pytest.mark.asyncio
async def test_async_error_types():
    async def raises_error() -> str:
        raise RuntimeError("test error")

    wrapped = gsta(raises_error)
    result, error = await wrapped()
    assert result is None
    assert isinstance(error, ErrorInfo)
    assert isinstance(error.exception, RuntimeError)
    assert isinstance(error.traceback, str)


# Decorator tests
@gst
def decorated_sync() -> int:
    return 123


@gsta
async def decorated_async() -> str:
    return "decorated"


@pytest.mark.asyncio
async def test_decorator_sync_types():
    result, error = decorated_sync()
    assert isinstance(result, int)
    assert error is None


@pytest.mark.asyncio
async def test_decorator_async_types():
    result, error = await decorated_async()
    assert isinstance(result, str)
    assert error is None
