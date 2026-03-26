"""Base model classes for HELIOS data structures."""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, ClassVar, Dict, Optional, Type, TypeVar
import json

T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    """Lightweight base class for serialisable records."""

    _registry: ClassVar[Dict[str, Type[BaseModel]]] = {}

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        # TODO: add support for custom JSON encoders (datetime, Decimal, etc.)
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls: Type[T], data: dict) -> T:
        # TODO: validate required fields and raise descriptive errors on missing keys
        return cls(**data)

    @classmethod
    def from_json(cls: Type[T], raw: str) -> T:
        return cls.from_dict(json.loads(raw))

    @classmethod
    def register(cls, name: str):
        """Class decorator to register a model by name."""
        def decorator(klass):
            cls._registry[name] = klass
            return klass
        return decorator


@dataclass
class Event(BaseModel):
    event_type: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    source: Optional[str] = None
    # TODO: add monotonic sequence number for ordering guarantees


@dataclass
class MetricPoint(BaseModel):
    name: str = ""
    value: float = 0.0
    tags: Dict[str, str] = field(default_factory=dict)
    # TODO: replace float timestamp with timezone-aware datetime
    timestamp: float = 0.0
