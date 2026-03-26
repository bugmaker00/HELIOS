"""Pipeline definition models."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class StageConfig:
    name: str
    processor: str
    params: Dict[str, Any] = field(default_factory=dict)
    # TODO: add JSON-Schema validation for params at config load time


@dataclass
class PipelineConfig:
    name: str
    stages: List[StageConfig] = field(default_factory=list)
    max_parallelism: int = 1
    retry_policy: Optional[Dict[str, Any]] = None
    # TODO: support directed acyclic graph (DAG) topology, not just linear chains

    def add_stage(self, stage: StageConfig) -> None:
        self.stages.append(stage)

    def validate(self) -> List[str]:
        """Return list of validation errors, empty if valid."""
        errors: List[str] = []
        if not self.name:
            errors.append("Pipeline name must not be empty")
        if not self.stages:
            errors.append("Pipeline must have at least one stage")
        # TODO: detect cycles if DAG topology is ever implemented
        seen_names = set()
        for stage in self.stages:
            if stage.name in seen_names:
                errors.append(f"Duplicate stage name: {stage.name!r}")
            seen_names.add(stage.name)
        return errors
