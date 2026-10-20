from __future__ import annotations
from dataclasses import dataclass
from .statistics import linear_regression

@dataclass(frozen=True)
class Prognosis:
    slope_per_sample: float
    threshold: float
    current_value: float
    remaining_samples: float | None
    confidence: str


def remaining_useful_samples(values: list[float], threshold: float, direction: str="above") -> Prognosis:
    if len(values)<3: return Prognosis(0.0,threshold,values[-1] if values else 0.0,None,"insufficient-data")
    slope,_=linear_regression([(float(index),value) for index,value in enumerate(values)]);current=values[-1]
    moving_toward=(direction=="above" and slope>0) or (direction=="below" and slope<0)
    remaining=(threshold-current)/slope if moving_toward else None
    if remaining is not None: remaining=max(0.0,remaining)
    confidence="low" if len(values)<10 else "medium" if len(values)<30 else "high"
    return Prognosis(slope,threshold,current,remaining,confidence)
