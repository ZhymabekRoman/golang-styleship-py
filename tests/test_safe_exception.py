import pytest
import asyncio
from golang_styleship_py.safe_exception import (
    go_style_func,
    go_style_func_async,
    go_style_decorator,
    gst,
    gsta,
    gstdec,
)


def test_sync_function():
    def add(a, b):
        return a + b

    result, error = go_style_func(add)(2, 3)
    assert result == 5
    assert error is None


def test_sync_function_error():
    def divide(a, b):
        return a / b

    result, error = go_style_func(divide)(1, 0)
    assert result is None
    assert isinstance(error, ZeroDivisionError)


@pytest.mark.asyncio
async def test_async_function():
    async def async_add(a, b):
        return a + b

    result, error = await go_style_func_async(async_add)(2, 3)
    assert result == 5
    assert error is None


@pytest.mark.asyncio
async def test_async_function_error():
    async def async_divide(a, b):
        return a / b

    result, error = await go_style_func_async(async_divide)(1, 0)
    assert result is None
    assert isinstance(error, ZeroDivisionError)


def test_decorator_sync():
    @go_style_decorator
    def multiply(a, b):
        return a * b

    result, error = multiply(2, 3)
    assert result == 6
    assert error is None


@pytest.mark.asyncio
async def test_decorator_async():
    @go_style_decorator
    async def async_multiply(a, b):
        return a * b

    result, error = await async_multiply(2, 3)
    assert result == 6
    assert error is None


class TestMethods:
    def test_instance_method(self):
        class Math:
            @go_style_decorator
            def add(self, a, b):
                return a + b

        math = Math()
        result, error = math.add(2, 3)
        assert result == 5
        assert error is None

    def test_static_method(self):
        class Math:
            @staticmethod
            @go_style_decorator
            def multiply(a, b):
                return a * b

        result, error = Math.multiply(2, 3)
        assert result == 6
        assert error is None

    @pytest.mark.asyncio
    async def test_async_instance_method(self):
        class AsyncMath:
            @go_style_decorator
            async def add(self, a, b):
                return a + b

        math = AsyncMath()
        result, error = await math.add(2, 3)
        assert result == 5
        assert error is None

    def test_class_method(self):
        class Math:
            @classmethod
            @go_style_decorator
            def multiply(cls, a, b):
                return a * b

        result, error = Math.multiply(2, 3)
        assert result == 6
        assert error is None

    @pytest.mark.asyncio
    async def test_async_class_method(self):
        class AsyncMath:
            @classmethod
            @go_style_decorator
            async def divide(cls, a, b):
                return a / b

        result, error = await AsyncMath.divide(6, 2)
        assert result == 3
        assert error is None

    def test_class_method_error(self):
        class Math:
            @classmethod
            @go_style_decorator
            def divide(cls, a, b):
                return a / b

        result, error = Math.divide(1, 0)
        assert result is None
        assert isinstance(error, ZeroDivisionError)

    def test_divide_function(self):
        def divide(a, b):
            return a / b

        result, error = gst(divide)(2, 0)
        assert result is None
        assert isinstance(error, ZeroDivisionError)

    @pytest.mark.asyncio
    async def test_async_class_method_error(self):
        class AsyncMath:
            @classmethod
            @go_style_decorator
            async def divide(cls, a, b):
                return a / b

        result, error = await AsyncMath.divide(1, 0)
        assert result is None
        assert isinstance(error, ZeroDivisionError)

    def test_static_method_error(self):
        class Math:
            @staticmethod
            @go_style_decorator
            def divide(a, b):
                return a / b

        result, error = Math.divide(1, 0)
        assert result is None
        assert isinstance(error, ZeroDivisionError)

    @pytest.mark.asyncio
    async def test_async_static_method(self):
        class AsyncMath:
            @staticmethod
            @go_style_decorator
            async def multiply(a, b):
                await asyncio.sleep(0.01)
                return a * b

        result, error = await AsyncMath.multiply(2, 3)
        assert result == 6
        assert error is None

    @pytest.mark.asyncio
    async def test_async_static_method_error(self):
        class AsyncMath:
            @staticmethod
            @go_style_decorator
            async def divide(a, b):
                await asyncio.sleep(0.01)
                return a / b

        result, error = await AsyncMath.divide(1, 0)
        assert result is None
        assert isinstance(error, ZeroDivisionError)

    def test_class_method_with_cls(self):
        class Math:
            multiplier = 2

            @classmethod
            @go_style_decorator
            def multiply(cls, a):
                return a * cls.multiplier

        result, error = Math.multiply(3)
        assert result == 6
        assert error is None

    @pytest.mark.asyncio
    async def test_async_class_method_with_cls(self):
        class AsyncMath:
            divisor = 2

            @classmethod
            @go_style_decorator
            async def divide(cls, a):
                await asyncio.sleep(0.01)
                return a / cls.divisor

        result, error = await AsyncMath.divide(6)
        assert result == 3
        assert error is None


def test_gst_alias():
    def subtract(a, b):
        return a - b

    result, error = gst(subtract)(5, 3)
    assert result == 2
    assert error is None


@pytest.mark.asyncio
async def test_gsta_alias():
    async def async_subtract(a, b):
        return a - b

    result, error = await gsta(async_subtract)(5, 3)
    assert result == 2
    assert error is None


def test_gstdec_alias():
    @gstdec
    def divide(a, b):
        return a / b

    result, error = divide(6, 3)
    assert result == 2
    assert error is None


def test_nested_go_style_functions():
    @go_style_decorator
    def outer(x):
        @go_style_decorator
        def inner(y):
            return y * 2

        result, error = inner(x)
        return result + 1 if result else None

    result, error = outer(5)
    assert result == 11
    assert error is None


@pytest.mark.asyncio
async def test_async_generator():
    @go_style_decorator
    async def async_generator():
        for i in range(3):
            await asyncio.sleep(0.01)
            yield i

    result, error = async_generator()
    assert error is None
    print(result)
    assert [item async for item in result] == [0, 1, 2]


@pytest.mark.asyncio
async def test_concurrent_async_calls():
    @go_style_decorator
    async def async_task(x):
        await asyncio.sleep(0.1)
        return x * 2

    tasks = [async_task(i) for i in range(5)]
    results = await asyncio.gather(*tasks)

    for i, (result, error) in enumerate(results):
        assert error is None
        matching_result = i * 2
        assert result == matching_result
