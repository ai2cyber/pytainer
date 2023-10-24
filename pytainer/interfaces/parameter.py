from typing import Generic, Type, TypeVar

_T = TypeVar("_T")


class Parameter(Generic[_T]):
    def __init__(self, name: str, _type: Type[_T]) -> None:
        self.name: str = name
        self.type: Type[_T] = _type
