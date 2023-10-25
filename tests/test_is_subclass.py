import unittest
from typing import Any, Dict, Generic, List, Mapping, Tuple, Type, TypeVar

from pytainer.utilities import is_subclass

_T = TypeVar("_T")


class IService(Generic[_T]):
    pass


class Service(Generic[_T], IService[_T]):
    pass


class TestIsSubclass(unittest.TestCase):
    def test_is_subclass(self) -> None:
        cases: List[Tuple[Type[IService[Any]], Type[IService[Any]], bool]] = [
            # ! Simple types probably with generics
            (Service, IService, True),
            (Service[int], IService[int], True),
            (Service[str], IService[int], False),
            # ! Dict can be assigned to Mapping but not the other way around
            (Service[Dict[str, int]], IService[Dict[str, int]], True),
            (Service[Dict[str, int]], IService[Mapping[str, int]], True),
            (Service[Mapping[str, int]], IService[Dict[str, int]], False),
            # ! Works with deeply nested types
            (Service[Dict[str, Dict[str, int]]], IService[Dict[str, Dict[str, int]]], True),
            (Service[Dict[str, Dict[str, int]]], IService[Mapping[str, Mapping[str, int]]], True),
            (Service[Mapping[str, Mapping[str, int]]], IService[Dict[str, Dict[str, int]]], False),
        ]

        for child, parent, truth in cases:
            self.assertEqual(is_subclass(child, parent), truth)


if __name__ == "__main__":
    unittest.main()
