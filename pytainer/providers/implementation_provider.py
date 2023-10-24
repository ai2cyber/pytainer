from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from pytainer.exceptions import ResolutionException, VerificationException
from pytainer.interfaces import IContainer, Parameter, Provider
from pytainer.lifecycle import Lifecycle
from pytainer.utilities import extract_constructor, is_subclass

_T = TypeVar("_T")


class ImplementationProvider(Generic[_T], Provider[_T]):
    def __init__(self, service: Type[_T], implementation: Type[_T], lifecycle: Lifecycle = Lifecycle.Transient) -> None:
        super().__init__(service, lifecycle)
        self.implementation = implementation
        self.dependencies: List[Parameter[Any]] = extract_constructor(self.implementation.__init__)

    def __exception(self, reason: str) -> VerificationException:
        return VerificationException(self.service, reason)

    def verify(self, container: IContainer) -> Optional[VerificationException]:
        if not is_subclass(self.implementation, self.service):
            return self.__exception(f'Implementation "{self.implementation}" is not subclass of "{self.service}"')

        for dependency in self.dependencies:
            is_registered = container.is_registered(dependency.type)
            if not is_registered:
                return self.__exception(f"{self.implementation} depends on {dependency.type} but it's not registered.")
        return None

    def __construct(self, container: IContainer) -> _T:
        constructor_args: Dict[str, Any] = {}

        for dependency in self.dependencies:
            constructor_args[dependency.name] = container.resolve(dependency.type)

        return self.implementation(**constructor_args)

    def resolve(self, container: IContainer) -> _T:
        try:
            return_instance = self.lifecycle is Lifecycle.Singleton

            if return_instance and not self.instance:
                self.instance = self.__construct(container)

            return self.instance if return_instance and self.instance else self.__construct(container)
        except Exception as e:
            raise ResolutionException(self.service, str(e))
