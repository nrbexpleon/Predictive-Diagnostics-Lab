from __future__ import annotations
import csv,json
from pathlib import Path
from .models import TelemetryDataset,TelemetryRecord

def load_json(path:str|Path)->dict:return json.loads(Path(path).read_text(encoding="utf-8"))
def load_json_dataset(path:str|Path)->TelemetryDataset:
    payload=load_json(path);return dataset_from_dict(payload)
def dataset_from_dict(payload:dict)->TelemetryDataset:
    return TelemetryDataset(str(payload.get("name","dataset")),str(payload.get("version","0")),tuple(TelemetryRecord(str(item["vehicle_id"]),int(item["timestamp_ms"]),str(item["software_version"]),str(item["variant"]),{str(k):float(v) for k,v in item["values"].items()},str(item.get("trip_id","default")),str(item.get("cohort","default")),dict(item.get("metadata",{}))) for item in payload["records"]))
def load_csv_dataset(path:str|Path,name:str="csv-dataset",version:str="0")->TelemetryDataset:
    rows=[]
    with Path(path).open(newline="",encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            identity={key:row.pop(key) for key in ["vehicle_id","timestamp_ms","software_version","variant","trip_id","cohort"]};rows.append(TelemetryRecord(identity["vehicle_id"],int(identity["timestamp_ms"]),identity["software_version"],identity["variant"],{key:float(value) for key,value in row.items() if value!=""},identity["trip_id"],identity["cohort"]))
    return TelemetryDataset(name,version,tuple(rows))
