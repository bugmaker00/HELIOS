"""Tests for the Scheduler."""

import time
import pytest
from helios.core.scheduler import Scheduler


class TestScheduler:
    def test_schedule_and_tick(self):
        scheduler = Scheduler()
        called = []
        scheduler.schedule(0.0, called.append, "hello")
        count = scheduler.tick()
        assert count == 1
        assert called == ["hello"]

    def test_pending_count(self):
        scheduler = Scheduler()
        scheduler.schedule(1000.0, lambda: None)  # far future
        assert scheduler.pending() == 1
        # TODO: add test for cancellation once cancel() is implemented

    def test_exception_in_task(self):
        scheduler = Scheduler()
        def bad():
            raise RuntimeError("boom")
        scheduler.schedule(0.0, bad)
        # Should not raise; exception is swallowed into dead-letter queue
        # TODO: assert the exception landed in the dead-letter queue
        count = scheduler.tick()
        assert count == 0  # failed task doesn't count as "ran"
