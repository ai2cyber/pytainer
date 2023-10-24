from abc import ABC, abstractmethod
from typing import Generic, Optional, Type, TypeVar

from pytainer.exceptions import VerificationException
from pytainer.interfaces.container import IContainer
from pytainer.lifecycle import Lifecycle

_T = TypeVar("_T")


class Provider(ABC, Generic[_T]):
    def __init__(self, service: Type[_T], lifecycle: Lifecycle, instance: Optional[_T] = None) -> None:
        self.service: Type[_T] = service
        self.lifecycle: Lifecycle = lifecycle
        self.instance: Optional[_T] = instance

    @abstractmethod
    def verify(self, container: IContainer) -> Optional[VerificationException]:
        raise NotImplementedError()

    @abstractmethod
    def resolve(self, container: IContainer) -> _T:
        raise NotImplementedError()
