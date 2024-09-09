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

### Synchronous decorator

```python
from golang_styleship_py import go_style_decorator, gstdec

@go_style_decorator # or @gstdec
def divide(a, b):
    return a / b

result, error = divide(10, 2)
print(result)  # Output: 5
print(error)  # Output: None
```

### Asynchronous decorator

```python
from golang_styleship_py import go_style_decorator, gstdec

@go_style_decorator # or @gstdec
async def async_divide(a, b):
    return a / b

result, error = await async_divide(2, 0)
print(result)  # Output: None
print(error)  # Output: Exception: Division by zero
```

### Synchronous function

```python
from golang_styleship_py import go_style_func, gst

def divide(a, b):
    return a / b

result, error = gst(divide)(2, 0)
print(result)  # Output: None
print(error)  # Output: Exception: Division by zero
```

### Asynchronous function

```python
from golang_styleship_py import go_style_func_async, gsta

async def async_divide(a, b):
    return a / b

result, error = await gsta(async_divide)(2, 0)
print(result)  # Output: None
print(error)  # Output: Exception: Division by zero
```
