from typing import Tuple


def get_generic_bases(_type: type) -> Tuple[type, ...]:
    return getattr(_type, "__orig_bases__", ())
