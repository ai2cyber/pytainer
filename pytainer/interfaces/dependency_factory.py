from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from pytainer.interfaces.container import IContainer

_T = TypeVar("_T", covariant=True)


class DependencyFactory(Protocol[_T]):
    def __call__(self, container: "IContainer") -> _T:
        ...
