import inspect
from typing import Any, Callable, List

from pytainer.interfaces import Parameter
from pytainer.utilities.map_to import map_to


def extract_constructor(function: Callable[[Any], Any]) -> List[Parameter[Any]]:
    parameters = inspect.signature(function).parameters
    filtered_parameters = [parameters[name] for name in parameters if parameters[name].annotation is not inspect.Parameter.empty]

    return map_to(filtered_parameters, lambda p: Parameter(p.name, p.annotation))
