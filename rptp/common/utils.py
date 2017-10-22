from typing import Iterator, Any


def last(iterator: Iterator[Any], default: Any = None) -> Any:
    """
    Returns last element of iterable.

    >>> last(iter([1, 2, 3]))
    3
    """

    result = default

    for result in iterator:
        pass

    return result
