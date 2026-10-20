from __future__ import annotations
from dataclasses import dataclass
from statistics import median
from .statistics import mad, mean, stdev

@dataclass(frozen=True)
class Detection:
    index: int
    score: float
    method: str
    actual: float
    baseline: float


def robust_zscore(values: list[float], baseline_count: int, threshold: float) -> list[Detection]:
    baseline = values[:baseline_count]; centre = median(baseline); scale = mad(baseline) * 1.4826
    if scale == 0: scale = stdev(baseline) or 1e-12
    return [Detection(index, abs(value-centre)/scale, "robust-zscore", value, centre) for index,value in enumerate(values) if index >= baseline_count and abs(value-centre)/scale >= threshold]


def ewma(values: list[float], baseline_count: int, alpha: float, threshold: float) -> list[Detection]:
    baseline = values[:baseline_count]; centre = mean(baseline); sigma = stdev(baseline) or 1e-12; state = centre; found=[]
    for index,value in enumerate(values):
        state = alpha*value + (1-alpha)*state
        score = abs(state-centre)/(sigma*(alpha/(2-alpha))**0.5)
        if index >= baseline_count and score >= threshold: found.append(Detection(index,score,"ewma",value,centre))
    return found


def cusum(values: list[float], baseline_count: int, drift: float, threshold: float) -> list[Detection]:
    baseline=values[:baseline_count]; centre=mean(baseline); sigma=stdev(baseline) or 1e-12; positive=negative=0.0; found=[]
    for index,value in enumerate(values):
        normalized=(value-centre)/sigma;positive=max(0.0,positive+normalized-drift);negative=min(0.0,negative+normalized+drift);score=max(positive,-negative)
        if index>=baseline_count and score>=threshold: found.append(Detection(index,score,"cusum",value,centre));positive=negative=0.0
    return found
