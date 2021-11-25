# typecheck
A simple decorator to validate the types of function arguments

### Limitations
Currently, it only supports Python objects where `isinstance` checks are all you have to do.
When I find a clean way of adding checks for `typing` hints, I'll probably add those in too.
It also doesn't care about validating the output type because that would add enormous complexity I have no interest in implementing.

### Examples
##### Basic usage
```python
from typecheck import typecheck

@typecheck
def fnc(x: int):
    print("Hi" * x)

fnc(3)
# HiHiHi

fnc("2")
# TypeCheckError: Param x expected <class 'int'> but received <class 'str'>
```

##### Missing arguments
```python
@typecheck
def fnc(x: int):
    print("Hi" * x)

fnc()
# TypeCheckError: Callable takes positional argument(s) ['x'], but was given ()
```

##### args and kwargs validation
```python
@typecheck
def fnc(*args: int, **kwargs: float):
    return sum(args) + sum(kwargs.values())

fnc(1, 2, 3, pi=3.14, e=2.72)
# 11.86

fnc(1, 2, 3, pi=3.14, e=2)
# TypeCheckError: varkw must all be of type <class 'float'>
```
