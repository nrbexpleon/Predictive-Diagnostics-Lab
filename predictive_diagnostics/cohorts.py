from __future__ import annotations
from collections import defaultdict
from .statistics import mean

def cohort_summary(records, signal_id: str) -> dict[str,dict[str,float]]:
    groups=defaultdict(list)
    for record in records:
        if signal_id in record.values: groups[f"{record.variant}|{record.software_version}|{record.cohort}"].append(record.values[signal_id])
    return {name:{"count":float(len(values)),"mean":mean(values),"minimum":min(values),"maximum":max(values)} for name,values in groups.items()}

def cohort_deviation(summaries: dict[str,dict[str,float]]) -> list[dict[str,float|str]]:
    if len(summaries)<2:return []
    global_mean=mean([item["mean"] for item in summaries.values()]);return [{"cohort":name,"mean":item["mean"],"deviation":item["mean"]-global_mean} for name,item in summaries.items()]
