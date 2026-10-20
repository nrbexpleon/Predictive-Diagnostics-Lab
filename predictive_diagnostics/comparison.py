from __future__ import annotations

def compare_reports(baseline:dict,candidate:dict)->dict:
    baseline_causes={(x["software_version"],x["variant"],x["signal_id"]):x for x in baseline["root_causes"]};candidate_causes={(x["software_version"],x["variant"],x["signal_id"]):x for x in candidate["root_causes"]};keys=set(baseline_causes)|set(candidate_causes)
    return {"baseline_run_id":baseline["run_id"],"candidate_run_id":candidate["run_id"],"finding_count_delta":candidate["finding_count"]-baseline["finding_count"],"decision_changed":baseline["decision"]!=candidate["decision"],"cohort_changes":[{"software_version":key[0],"variant":key[1],"signal_id":key[2],"affected_vehicle_delta":candidate_causes.get(key,{}).get("affected_vehicles",0)-baseline_causes.get(key,{}).get("affected_vehicles",0),"finding_delta":candidate_causes.get(key,{}).get("finding_count",0)-baseline_causes.get(key,{}).get("finding_count",0)} for key in sorted(keys)]}
