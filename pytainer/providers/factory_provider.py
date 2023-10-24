from typing import Generic, Optional, Type, TypeVar

from pytainer.exceptions import ResolutionException, VerificationException
from pytainer.interfaces import DependencyFactory, IContainer, Provider
from pytainer.lifecycle import Lifecycle
from pytainer.utilities import is_subclass

_T = TypeVar("_T")


class FactoryProvider(Generic[_T], Provider[_T]):
    def __init__(self, service: Type[_T], factory: DependencyFactory[_T]) -> None:
        super().__init__(service, Lifecycle.Transient)
        self.factory = factory

    def __exception(self, reason: str) -> VerificationException:
        return VerificationException(self.service, reason)

    def verify(self, container: IContainer) -> Optional[VerificationException]:
        container.verified = True

        try:
            instance = self.factory(container)
            if not is_subclass(type(instance), self.service):
                return self.__exception(f"Return type of factory is not instance of {self.service}.")
        except Exception as ex:
            return self.__exception(str(ex))
        finally:
            container.verified = False

        return None

    def resolve(self, container: IContainer) -> _T:
        try:
            return_instance = self.lifecycle is Lifecycle.Singleton

            if return_instance and not self.instance:
                self.instance = self.factory(container)

            return self.instance if return_instance and self.instance else self.factory(container)
        except Exception as e:
            raise ResolutionException(self.service, str(e))
