from typing import Optional, Tuple, Any


def get_multi_attr(target: Any, /, *keys: str, default: Any = None) -> Tuple[Optional[Any], ...]:
    return tuple(getattr(target, key, default) for key in keys)


def is_function(target: Any, /) -> bool:
    """checks if callable is normal function and not class method"""
    name, qualifier = get_multi_attr(target, '__name__', '__qualname__')
    return name and name == qualifier


def is_method(target, /) -> bool:
    """check if callable is class method"""
    name, qualifier = get_multi_attr(target, '__name__', '__qualname__')
    qualifier_parts = qualifier.split('.')
    return len(qualifier_parts) == 2 and qualifier_parts[1] == name
