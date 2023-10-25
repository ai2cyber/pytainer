import unittest
from abc import ABC, abstractmethod

from pytainer import Container, Lifecycle, RegistrationException, ResolutionException


class IService(ABC):
    @abstractmethod
    def state(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def modify_state(self, state: str) -> None:
        raise NotImplementedError


class Service(IService):
    def __init__(self) -> None:
        self._state: str = "This is a test"

    def state(self) -> str:
        return self._state

    def modify_state(self, state: str) -> None:
        self._state = state


class TestContainer(unittest.TestCase):
    def test_implementation_registration_singleton(self) -> None:
        container = Container()
        container.register_implementation(IService, Service, Lifecycle.Singleton)
        container.verify()

        instance = container.resolve(IService)
        other_instance = container.resolve(IService)

        self.assertIsInstance(instance, Service)
        self.assertEqual("This is a test", instance.state())

        self.assertIsInstance(other_instance, Service)
        self.assertEqual("This is a test", other_instance.state())

        self.assertEqual(instance, other_instance)

    def test_implementation_registration_transient(self) -> None:
        container = Container()
        container.register_implementation(IService, Service, Lifecycle.Transient)
        container.verify()

        instance = container.resolve(IService)
        other_instance = container.resolve(IService)

        self.assertIsInstance(instance, Service)
        self.assertEqual("This is a test", instance.state())

        self.assertIsInstance(other_instance, Service)
        self.assertEqual("This is a test", other_instance.state())

        self.assertNotEqual(instance, other_instance)

    def test_instance_registration(self) -> None:
        container = Container()
        container.register_instance(IService, Service())
        container.verify()

        instance = container.resolve(IService)
        other_instance = container.resolve(IService)

        self.assertIsInstance(instance, Service)
        self.assertEqual("This is a test", instance.state())

        self.assertIsInstance(other_instance, Service)
        self.assertEqual("This is a test", other_instance.state())

        self.assertEqual(instance, other_instance)

    def test_factory_registration(self) -> None:
        container = Container()
        container.register_factory(IService, lambda container: Service())
        container.verify()

        instance = container.resolve(IService)
        other_instance = container.resolve(IService)

        self.assertIsInstance(instance, Service)
        self.assertEqual("This is a test", instance.state())

        self.assertIsInstance(other_instance, Service)
        self.assertEqual("This is a test", other_instance.state())

        self.assertNotEqual(instance, other_instance)

    def test_resolution_before_verification(self) -> None:
        container = Container()

        with self.assertRaises(ResolutionException):
            container.resolve(IService)

    def test_registration_after_verification(self) -> None:
        container = Container()
        container.verify()

        with self.assertRaises(RegistrationException):
            container.register_implementation(IService, Service)

    def test_unregistered_resolution(self) -> None:
        container = Container()
        container.verify()

        with self.assertRaises(ResolutionException):
            container.resolve(IService)

    def test_singleton_instance_lifetime(self) -> None:
        container = Container()
        container.register_implementation(IService, Service, Lifecycle.Singleton)
        container.verify()

        instance = container.resolve(IService)
        other_instance = container.resolve(IService)

        # The same instance should be returned for a Singleton.
        self.assertEqual(instance, other_instance)

        # Modifying one instance should affect the other.
        instance.modify_state("New State")
        self.assertEqual(other_instance.state(), "New State")

    def test_transient_instance_lifetime(self) -> None:
        container = Container()
        container.register_implementation(IService, Service, Lifecycle.Transient)
        container.verify()

        instance = container.resolve(IService)
        other_instance = container.resolve(IService)

        # Transient instances should not be the same.
        self.assertNotEqual(instance, other_instance)

        # Modifying one instance should not affect the other.
        instance.modify_state("New State")
        self.assertNotEqual(other_instance.state(), "New State")


if __name__ == "__main__":
    unittest.main()
