from typing import Protocol, Any


class StateEngineProtocol(Protocol):
    """
    Protocol for a hierarchical, thread-safe state store.

    Provides dot-separated path access.
    """

    def set(self, path: str, value: Any) -> None:
        """
        Set a value in the state at the given dot-separated path.

        Args:
            path: Dot-separated key path (e.g., "system.clock.uptime")
            value: Value to store
        """
        ...

    def get(self, path: str, default: Any = None) -> Any:
        """
        Retrieve a value from the state at the given dot-separated path.

        Args:
            path: Dot-separated key path
            default: Value to return if path is not found

        Returns:
            The stored value or `default` if not found
        """
        ...
