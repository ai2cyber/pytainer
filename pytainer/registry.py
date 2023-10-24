from typing import Any, Dict, List, Optional

from pytainer.interfaces import Provider
from pytainer.utilities import last_or_default


class Registry:
    def __init__(self) -> None:
        self._registry: Dict[type, List[Provider[Any]]] = {}

    def get(self, service: type) -> Optional[Provider[Any]]:
        self.__ensure_existence(service)
        return last_or_default(self._registry[service])

    def get_all(self, service: type) -> List[Provider[Any]]:
        self.__ensure_existence(service)
        return self._registry[service]

    def set(self, service: type, registration: Provider[Any]) -> None:
        self.__ensure_existence(service)
        self._registry[service].append(registration)

    def set_all(self, service: type, registrations: List[Provider[Any]]) -> None:
        self._registry[service] = registrations

    def has(self, service: type) -> bool:
        return service in self._registry

    def __ensure_existence(self, service: type) -> None:
        if not self.has(service):
            self._registry[service] = []

    def __del__(self) -> None:
        del self._registry
