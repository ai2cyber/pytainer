from typing import Callable, List, TypeVar

_T = TypeVar("_T")
_P = TypeVar("_P")


def map_to(lst: List[_T], mapping: Callable[[_T], _P]) -> List[_P]:
    return [mapping(item) for item in lst]
