import threading
from typing import Optional

from .runtime import Runtime


class ThreadedRuntime(Runtime):
    """
    Runtime variant that owns a background execution thread.

    - boot() and shutdown() remain synchronous
    - run() blocks the caller until shutdown
    - No OS signals required
    """

    def _on_boot(self) -> None:
        self._stop_event = threading.Event()
        super()._on_boot()

    def run(self) -> None:
        """
        Boot the runtime and block until shutdown is complete.
        """
        self._stop_event.clear()

        with self:
            self._run_thread = threading.current_thread()
            self._stop_event.wait()

    def shutdown(self, reason: Optional[str] = None) -> None:
        """
        Signal the runtime thread to exit, then perform shutdown.
        """
        if not self.booted:
            return

        try:
            super().shutdown(reason=reason)
        finally:
            self._stop_event.set()
