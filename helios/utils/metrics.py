"""Lightweight metrics collection."""

import time
from collections import defaultdict
from typing import Dict, List


class Counter:
    def __init__(self):
        self._value: float = 0.0

    def inc(self, delta: float = 1.0) -> None:
        self._value += delta

    @property
    def value(self) -> float:
        return self._value


class Histogram:
    """Record a distribution of values."""

    DEFAULT_BUCKETS = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]

    def __init__(self, buckets: List[float] = None):
        self._buckets = sorted(buckets or self.DEFAULT_BUCKETS)
        self._counts: Dict[float, int] = {b: 0 for b in self._buckets}
        self._sum: float = 0.0
        self._count: int = 0
        # TODO: add support for exemplars (OpenMetrics 1.0)

    def observe(self, value: float) -> None:
        self._sum += value
        self._count += 1
        for b in self._buckets:
            if value <= b:
                self._counts[b] += 1

    @property
    def mean(self) -> float:
        return self._sum / self._count if self._count else 0.0


class MetricsRegistry:
    """Global registry for all metrics."""

    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._histograms: Dict[str, Histogram] = {}
        # TODO: expose Prometheus /metrics endpoint for scraping

    def counter(self, name: str) -> Counter:
        if name not in self._counters:
            self._counters[name] = Counter()
        return self._counters[name]

    def histogram(self, name: str, buckets: List[float] = None) -> Histogram:
        if name not in self._histograms:
            self._histograms[name] = Histogram(buckets)
        return self._histograms[name]

    def snapshot(self) -> dict:
        # TODO: include histogram percentiles (p50, p95, p99) in snapshot output
        return {
            "counters": {k: v.value for k, v in self._counters.items()},
        }
