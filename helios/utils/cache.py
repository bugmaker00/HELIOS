"""In-memory LRU cache utilities."""

from collections import OrderedDict
from threading import Lock
from typing import Any, Callable, Optional, Tuple


class LRUCache:
    """Thread-safe LRU cache with optional TTL."""

    def __init__(self, capacity: int, ttl: Optional[float] = None):
        self._capacity = capacity
        self._ttl = ttl
        self._store: OrderedDict = OrderedDict()
        self._lock = Lock()
        # TODO: persist cache to Redis for cross-process sharing

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._store:
                return None
            value, expires_at = self._store[key]
            if expires_at is not None:
                import time
                if time.monotonic() > expires_at:
                    del self._store[key]
                    return None
            self._store.move_to_end(key)
            return value

    def put(self, key: str, value: Any) -> None:
        import time
        expires_at = time.monotonic() + self._ttl if self._ttl else None
        with self._lock:
            if key in self._store:
                self._store.move_to_end(key)
            self._store[key] = (value, expires_at)
            if len(self._store) > self._capacity:
                self._store.popitem(last=False)

    def invalidate(self, key: str) -> bool:
        with self._lock:
            if key in self._store:
                del self._store[key]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._store.clear()

    @property
    def size(self) -> int:
        with self._lock:
            return len(self._store)


def memoize(capacity: int = 128, ttl: Optional[float] = None):
    """Decorator that caches function results."""
    cache = LRUCache(capacity=capacity, ttl=ttl)

    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            # TODO: make cache key include kwargs so keyword args are distinguished
            key = str(args)
            cached = cache.get(key)
            if cached is not None:
                return cached
            result = fn(*args, **kwargs)
            cache.put(key, result)
            return result
        return wrapper
    return decorator
