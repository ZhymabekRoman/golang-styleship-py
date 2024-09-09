# Golang-styleship-py

A Python module that implements Go-style error handling for both synchronous and asynchronous functions.

## Installation

### PIP

```bash
pip install git+https://github.com/ZhymabekRoman/golang-styleship-py
```

### Poetry

```bash
poetry add git+https://github.com/ZhymabekRoman/golang-styleship-py
```

## Usage

The module now returns an ErrorInfo dataclass for errors, which contains both the exception and the full traceback.

### Synchronous decorator

```python
from golang_styleship_py import go_style_decorator, gstdec

@go_style_decorator # or @gstdec
def divide(a, b):
    return a / b

result, error = divide(10, 2)
print(result)  # Output: 5
print(error)  # Output: None

result, error = divide(10, 0)
print(result)  # Output: None
if error:
    print(f"Error type: {type(error.exception)}")  # Output: Error type: <class 'ZeroDivisionError'>
    print(f"Error message: {error.exception}")  # Output: Error message: division by zero
    print("Traceback:")
    print(error.traceback)  # This will print the full traceback
```

### Asynchronous decorator

```python
import asyncio
from golang_styleship_py import go_style_decorator, gstdec

@go_style_decorator # or @gstdec
async def async_divide(a, b):
    await asyncio.sleep(0.1)  # Simulate some async operation
    return a / b

async def main():
    result, error = await async_divide(10, 2)
    print(result)  # Output: 5
    print(error)  # Output: None

    result, error = await async_divide(10, 0)
    print(result)  # Output: None
    if error:
        print(f"Error type: {type(error.exception)}")  # Output: Error type: <class 'ZeroDivisionError'>
        print(f"Error message: {error.exception}")  # Output: Error message: division by zero
        print("Traceback:")
        print(error.traceback)  # This will print the full traceback

asyncio.run(main())
```

### Synchronous function

```python
from golang_styleship_py import go_style_func, gst

def divide(a, b):
    return a / b

result, error = gst(divide)(10, 2)
print(result)  # Output: 5
print(error)  # Output: None

result, error = gst(divide)(10, 0)
print(result)  # Output: None
if error:
    print(f"Error type: {type(error.exception)}")  # Output: Error type: <class 'ZeroDivisionError'>
    print(f"Error message: {error.exception}")  # Output: Error message: division by zero
    print("Traceback:")
    print(error.traceback)  # This will print the full traceback
```

### Asynchronous function

```python
import asyncio
from golang_styleship_py import go_style_func_async, gsta

async def async_divide(a, b):
    await asyncio.sleep(0.1)  # Simulate some async operation
    return a / b

async def main():
    result, error = await gsta(async_divide)(10, 2)
    print(result)  # Output: 5
    print(error)  # Output: None

    result, error = await gsta(async_divide)(10, 0)
    print(result)  # Output: None
    if error:
        print(f"Error type: {type(error.exception)}")  # Output: Error type: <class 'ZeroDivisionError'>
        print(f"Error message: {error.exception}")  # Output: Error message: division by zero
        print("Traceback:")
        print(error.traceback)  # This will print the full traceback

asyncio.run(main())
```

### Accessing the ErrorInfo

When an error occurs, you can access the full exception and traceback information from the ErrorInfo object:

```python
result, error = some_function()
if error:
    print(f"An error occurred: {error.exception}")
    print("Full traceback:")
    print(error.traceback)
```

This allows for more detailed error reporting and debugging while maintaining the Go-style error handling pattern.

## Testing

```bash
pytest -x
```
