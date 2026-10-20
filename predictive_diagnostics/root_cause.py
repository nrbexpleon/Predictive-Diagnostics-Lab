from __future__ import annotations
from collections import defaultdict

def correlate_findings(findings:list[dict])->list[dict]:
    groups=defaultdict(list)
    for finding in findings:groups[(finding["software_version"],finding["variant"],finding["signal_id"])].append(finding)
    hypotheses=[]
    for (version,variant,signal_id),items in groups.items():
        vehicles={item["vehicle_id"] for item in items};methods={item["method"] for item in items};confidence=min(.99,.35+.15*len(vehicles)+.1*len(methods));hypotheses.append({"software_version":version,"variant":variant,"signal_id":signal_id,"affected_vehicles":len(vehicles),"finding_count":len(items),"detectors":sorted(methods),"confidence":round(confidence,3),"hypothesis":f"{signal_id} deviation is concentrated in software {version}, variant {variant}"})
    return sorted(hypotheses,key=lambda item:(item["affected_vehicles"],item["finding_count"]),reverse=True)
