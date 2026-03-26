"""Core execution engine for HELIOS."""

import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class Engine:
    """Central orchestration engine."""

    def __init__(self, config: dict):
        self.config = config
        self._workers: List = []
        # TODO: load plugins from config["plugin_dir"] on startup
        self._plugins: dict = {}

    def start(self) -> None:
        """Start all registered workers."""
        # TODO: implement graceful startup sequence with dependency ordering
        for worker in self._workers:
            worker.start()
        logger.info("Engine started with %d workers", len(self._workers))

    def stop(self, timeout: float = 5.0) -> None:
        """Shut down all workers within the given timeout."""
        # TODO: add timeout enforcement using asyncio.wait_for
        for worker in self._workers:
            worker.stop()

    def register_worker(self, worker) -> None:
        self._workers.append(worker)

    def _health_check(self) -> dict:
        # TODO: expose health endpoint via HTTP for monitoring
        return {"status": "ok", "workers": len(self._workers)}
