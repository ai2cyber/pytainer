from typing import Callable, List, Optional, Type, TypeVar

from pytainer.exceptions import RegistrationException, ResolutionException, VerificationException
from pytainer.interfaces import DependencyFactory, IContainer, Provider
from pytainer.lifecycle import Lifecycle
from pytainer.providers import FactoryProvider, ImplementationProvider, InstanceProvider
from pytainer.registry import Registry

_T = TypeVar("_T")


class Container(IContainer):
    def __init__(self) -> None:
        super().__init__()
        self._registry: Registry = Registry()
        self._verification_cbs: List[Callable[[IContainer], Optional[VerificationException]]] = []

    # ! ======================= Registration Methods ======================= ! #
    def register_factory(self, service: Type[_T], factory: DependencyFactory[_T]) -> None:
        provider = FactoryProvider(service, factory)
        return self._register(service, provider)

    def register_instance(self, service: Type[_T], instance: _T) -> None:
        provider = InstanceProvider(service, instance)
        return self._register(service, provider)

    def register_implementation(self, service: Type[_T], implementation: Type[_T], lifecycle: Lifecycle = Lifecycle.Singleton) -> None:
        provider = ImplementationProvider(service, implementation, lifecycle)
        return self._register(service, provider)

    # ! ======================= Resolution Methods ======================= ! #
    def resolve(self, service: Type[_T]) -> _T:
        self.__verify_resolvancy(service)
        if provider := self._registry.get(service):
            return provider.resolve(self)

        raise ResolutionException(service, "Attempted to resolve unregistered type.")

    def resolve_all(self, service: Type[_T]) -> List[_T]:
        self.__verify_resolvancy(service)
        if providers := self._registry.get_all(service):
            return [provider.resolve(self) for provider in providers]

        raise ResolutionException(service, "Attempted to resolve unregistered type.")

    # ! ======================= Verification Methods ======================= ! #
    def is_registered(self, service: type) -> bool:
        return bool(self._registry.get(service))

    def verify(self) -> None:
        for callback in self._verification_cbs:
            if exception := callback(self):
                raise exception
        self.verified = True

    # ! ======================= Private Helper Methods ======================= ! #
    def _register(self, service: Type[_T], provider: Provider[_T]) -> None:
        self.__verify_registration(service)
        self._verification_cbs.append(provider.verify)
        self._registry.set(service, provider)

    def __verify_resolvancy(self, service: type):
        if not self.verified:
            raise ResolutionException(service, "Cannot resolve an instance before the container is verified.")

    def __verify_registration(self, service: type):
        if self.verified:
            raise RegistrationException(service, "Cannot register any service to a verified container.")
