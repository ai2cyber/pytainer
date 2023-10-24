from typing import Optional, Sequence, TypeVar

_T = TypeVar("_T")


def last_or_default(lst: Sequence[_T]) -> Optional[_T]:
    if len(lst) == 0:
        return None

    return lst[-1]
