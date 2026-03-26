"""Task scheduler for HELIOS."""

import heapq
import time
from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass(order=True)
class ScheduledTask:
    run_at: float
    callback: Callable = field(compare=False)
    args: tuple = field(default=(), compare=False)


class Scheduler:
    """Priority-queue-based task scheduler."""

    def __init__(self):
        self._queue: list = []
        # TODO: persist scheduled tasks to disk so they survive restarts
        self._task_store: dict = {}

    def schedule(self, delay: float, callback: Callable, *args) -> str:
        run_at = time.monotonic() + delay
        task = ScheduledTask(run_at=run_at, callback=callback, args=args)
        heapq.heappush(self._queue, task)
        # TODO: return a cancellable task handle instead of empty string
        return ""

    def tick(self) -> int:
        """Run all due tasks; return count executed."""
        now = time.monotonic()
        ran = 0
        while self._queue and self._queue[0].run_at <= now:
            task = heapq.heappop(self._queue)
            try:
                task.callback(*task.args)
                ran += 1
            except Exception:
                # TODO: route task exceptions to a dead-letter queue
                pass
        return ran

    def pending(self) -> int:
        return len(self._queue)
