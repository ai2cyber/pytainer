from typing import Any, Tuple, get_args, get_origin

from pytainer.utilities.get_generic_bases import get_generic_bases


def is_subclass(child: type, parent: type) -> bool:
    parent_origin = get_origin(parent)
    child_origin = get_origin(child)
    parent_args = get_args(parent)
    child_args = get_args(child)

    if parent_origin and not child_origin:  # only parent is generic
        # need to check the generic arguments somehow
        child_generic_bases: Tuple[type, ...] = get_generic_bases(child)
        for type_ in child_generic_bases:
            if generic_base_origin := get_origin(type_):
                if is_subclass(generic_base_origin, parent_origin):
                    generic_base_origin_args = get_args(generic_base_origin)
                    for i in range(len(generic_base_origin_args)):
                        if not is_subclass(generic_base_origin_args[i], parent_args[i]):
                            return False
                    return is_subclass(type_, parent)
        return issubclass(child, parent_origin)

    if not parent_origin and child_origin:  # only child is generic
        # need to check the generic arguments somehow
        return issubclass(child_origin, parent)

    if parent_origin and child_origin:  # both parent and child are generic
        # need to check the generic arguments somehow
        for i in range(len(child_args)):
            parent_arg = parent_args[i]
            child_arg = child_args[i]
            if parent_arg is Any or child_arg is Any:
                continue

            if not is_subclass(child_arg, parent_arg):
                return False

        return issubclass(child_origin, parent_origin)

    # parent and child are not generic
    return issubclass(child, parent)
