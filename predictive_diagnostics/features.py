from __future__ import annotations
from .statistics import mean, percentile, stdev, linear_regression

def window_features(values: list[float], timestamps: list[int]) -> dict[str,float]:
    if len(values)!=len(timestamps) or not values: raise ValueError("aligned non-empty series required")
    slope,_=linear_regression([(float(time),value) for time,value in zip(timestamps,values)])
    differences=[values[index]-values[index-1] for index in range(1,len(values))]
    return {"count":float(len(values)),"mean":mean(values),"stdev":stdev(values),"minimum":min(values),"maximum":max(values),"p95":percentile(values,.95),"slope_per_ms":slope,"mean_absolute_delta":mean([abs(value) for value in differences])}
