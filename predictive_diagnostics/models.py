from __future__ import annotations
from dataclasses import dataclass, field
from math import isfinite
from typing import Any

@dataclass(frozen=True)
class SignalDefinition:
    id: str
    unit: str
    minimum: float
    maximum: float
    safety_relevant: bool = False
    def validate(self, value: float) -> None:
        if not self.id or not self.unit: raise ValueError("signal id and unit required")
        if not isfinite(value): raise ValueError(f"{self.id} must be finite")
        if not self.minimum <= value <= self.maximum: raise ValueError(f"{self.id} outside range")

@dataclass(frozen=True)
class TelemetryRecord:
    vehicle_id: str
    timestamp_ms: int
    software_version: str
    variant: str
    values: dict[str, float]
    trip_id: str = "default"
    cohort: str = "default"
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class TelemetryDataset:
    name: str
    version: str
    records: tuple[TelemetryRecord, ...]
    def validate(self, catalogue: dict[str, SignalDefinition]) -> None:
        if not self.name or not self.version: raise ValueError("dataset identity required")
        if not 2 <= len(self.records) <= 1_000_000: raise ValueError("dataset requires 2..1000000 records")
        previous: dict[str, int] = {}
        for record in self.records:
            if not record.vehicle_id or not record.software_version or not record.variant: raise ValueError("record identity required")
            if record.timestamp_ms < 0: raise ValueError("timestamp must be non-negative")
            if record.timestamp_ms <= previous.get(record.vehicle_id, -1): raise ValueError("vehicle timestamps must increase")
            previous[record.vehicle_id] = record.timestamp_ms
            if not record.values: raise ValueError("signal values required")
            for signal_id, value in record.values.items():
                if signal_id not in catalogue: raise ValueError(f"unknown signal {signal_id}")
                catalogue[signal_id].validate(value)

@dataclass(frozen=True)
class AnalysisPolicy:
    baseline_fraction: float = 0.4
    robust_z_threshold: float = 4.0
    ewma_alpha: float = 0.25
    ewma_threshold: float = 3.0
    cusum_drift: float = 0.5
    cusum_threshold: float = 5.0
    trend_horizon_samples: int = 100
    minimum_cohort_size: int = 2
    def validate(self) -> None:
        if not 0.1 <= self.baseline_fraction <= 0.8: raise ValueError("baseline_fraction out of range")
        if not 0 < self.ewma_alpha <= 1: raise ValueError("ewma_alpha out of range")
        if min(self.robust_z_threshold, self.ewma_threshold, self.cusum_threshold) <= 0: raise ValueError("thresholds must be positive")
        if self.trend_horizon_samples < 1 or self.minimum_cohort_size < 1: raise ValueError("integer policy values must be positive")
