from __future__ import annotations
from collections import defaultdict
from dataclasses import asdict
from uuid import uuid4
from .cohorts import cohort_deviation, cohort_summary
from .detectors import cusum, ewma, robust_zscore
from .features import window_features
from .models import AnalysisPolicy, SignalDefinition, TelemetryDataset
from .prognosis import remaining_useful_samples
from .root_cause import correlate_findings

class DiagnosticAnalyzer:
    def __init__(self,catalogue:list[SignalDefinition],policy:AnalysisPolicy|None=None):
        self.catalogue={signal.id:signal for signal in catalogue};self.policy=policy or AnalysisPolicy();self.policy.validate()
    def analyze(self,dataset:TelemetryDataset,thresholds:dict[str,dict]|None=None)->dict:
        dataset.validate(self.catalogue);thresholds=thresholds or {};findings=[];features={};prognoses={}
        grouped=defaultdict(list)
        for record in dataset.records:
            for signal_id,value in record.values.items():grouped[(record.vehicle_id,signal_id)].append((record.timestamp_ms,value,record))
        for (vehicle_id,signal_id),series in grouped.items():
            series.sort();timestamps=[item[0] for item in series];values=[item[1] for item in series];baseline_count=max(2,min(len(values)-1,int(len(values)*self.policy.baseline_fraction)));features[f"{vehicle_id}|{signal_id}"]=window_features(values,timestamps)
            detections=robust_zscore(values,baseline_count,self.policy.robust_z_threshold)+ewma(values,baseline_count,self.policy.ewma_alpha,self.policy.ewma_threshold)+cusum(values,baseline_count,self.policy.cusum_drift,self.policy.cusum_threshold)
            unique={}
            for detection in detections:
                key=(detection.index,detection.method);record=series[detection.index][2];unique[key]={"id":f"{vehicle_id}:{signal_id}:{detection.method}:{detection.index}","vehicle_id":vehicle_id,"signal_id":signal_id,"timestamp_ms":record.timestamp_ms,"software_version":record.software_version,"variant":record.variant,"cohort":record.cohort,"method":detection.method,"score":detection.score,"actual":detection.actual,"baseline":detection.baseline,"severity":severity(detection.score,self.catalogue[signal_id].safety_relevant)}
            findings.extend(unique.values())
            if signal_id in thresholds:
                config=thresholds[signal_id];prognoses[f"{vehicle_id}|{signal_id}"]=asdict(remaining_useful_samples(values,float(config["threshold"]),str(config.get("direction","above"))))
        summaries={signal_id:cohort_summary(dataset.records,signal_id) for signal_id in self.catalogue};deviations={signal_id:cohort_deviation(summary) for signal_id,summary in summaries.items()};root_causes=correlate_findings(findings);priority=sorted(findings,key=lambda item:priority_score(item,root_causes),reverse=True)
        return {"run_id":str(uuid4()),"schema_version":"1.0","dataset":{"name":dataset.name,"version":dataset.version,"records":len(dataset.records),"vehicles":len({r.vehicle_id for r in dataset.records})},"policy":asdict(self.policy),"features":features,"findings":findings,"finding_count":len(findings),"root_causes":root_causes,"priorities":[{**item,"priority_score":priority_score(item,root_causes)} for item in priority],"cohorts":summaries,"cohort_deviations":deviations,"prognoses":prognoses,"decision":"investigation-required" if findings else "eligible-for-human-review"}

def severity(score:float,safety_relevant:bool)->str:
    if score>=8 or (safety_relevant and score>=5):return "critical"
    if score>=5:return "high"
    if score>=3:return "medium"
    return "low"

def priority_score(finding:dict,causes:list[dict])->float:
    weight={"critical":4,"high":3,"medium":2,"low":1}[finding["severity"]];affected=max((cause["affected_vehicles"] for cause in causes if cause["software_version"]==finding["software_version"]),default=1);return round(weight*min(finding["score"],10)*affected,3)
