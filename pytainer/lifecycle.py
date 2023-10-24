from enum import Enum


class Lifecycle(Enum):
    Singleton = "singleton"
    """A single instance of the registered dependency is stored in memory and used when injecting."""

    Transient = "transient"
    """A new instance of the registered dependency will be created every time it is being injected."""
