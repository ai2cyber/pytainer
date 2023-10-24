from typing import Generic, Optional, Type, TypeVar

from pytainer.exceptions import ResolutionException, VerificationException
from pytainer.interfaces import IContainer, Provider
from pytainer.lifecycle import Lifecycle

_T = TypeVar("_T")


class InstanceProvider(Generic[_T], Provider[_T]):
    def __init__(self, service: Type[_T], instance: _T) -> None:
        super().__init__(service, Lifecycle.Singleton, instance)

    def verify(self, container: IContainer) -> Optional[VerificationException]:
        if not isinstance(self.instance, self.service):
            reason = f'Instance "{self.instance.__class__.__name__}" is not subclass of "{self.service}"'
            return VerificationException(self.service, reason)
        return None

    def resolve(self, container: IContainer) -> _T:
        if not self.instance:
            raise ResolutionException(self.service, "No instance is registered.")
        return self.instance
