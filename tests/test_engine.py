"""Unit tests for the Engine class."""

import pytest
from helios.core.engine import Engine


def make_engine() -> Engine:
    return Engine(config={"plugin_dir": "/tmp/helios_plugins"})


class TestEngine:
    def test_start_empty(self):
        engine = make_engine()
        engine.start()  # should not raise

    def test_health_check(self):
        engine = make_engine()
        result = engine._health_check()
        assert result["status"] == "ok"
        assert result["workers"] == 0
        # TODO: assert plugin count once plugin loading is implemented

    def test_register_worker(self):
        # TODO: use a proper mock worker instead of a plain object
        engine = make_engine()
        engine.register_worker(object())
        assert len(engine._workers) == 1
