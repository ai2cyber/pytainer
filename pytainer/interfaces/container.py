from abc import ABC, abstractmethod
from typing import List, Type, TypeVar

from pytainer.interfaces.dependency_factory import DependencyFactory
from pytainer.lifecycle import Lifecycle

_T = TypeVar("_T")


class IContainer(ABC):
    def __init__(self) -> None:
        self.verified: bool = False

    @abstractmethod
    def register_implementation(self, service: Type[_T], implementation: Type[_T], lifecycle: Lifecycle = Lifecycle.Singleton) -> None:
        raise NotImplementedError()

    @abstractmethod
    def register_instance(self, service: Type[_T], instance: _T) -> None:
        raise NotImplementedError()

    @abstractmethod
    def register_factory(self, service: Type[_T], factory: DependencyFactory[_T]) -> None:
        raise NotImplementedError()

    @abstractmethod
    def resolve(self, service: Type[_T]) -> _T:
        raise NotImplementedError()

    @abstractmethod
    def resolve_all(self, service: Type[_T]) -> List[_T]:
        raise NotImplementedError()

    @abstractmethod
    def is_registered(self, service: type) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def verify(self) -> None:
        raise NotImplementedError()
