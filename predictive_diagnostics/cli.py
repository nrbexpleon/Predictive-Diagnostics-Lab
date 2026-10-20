from __future__ import annotations
import argparse,json
from dataclasses import asdict
from pathlib import Path
from .analyzer import DiagnosticAnalyzer
from .config import default_catalogue
from .evidence import create_evidence,verify_evidence
from .io import load_json_dataset
from .synthetic import generate_fleet

def main()->int:
    parser=argparse.ArgumentParser(description="Predictive Diagnostics Lab");parser.add_argument("--dataset");parser.add_argument("--vehicles",type=int,default=100);parser.add_argument("--samples",type=int,default=40);parser.add_argument("--output");args=parser.parse_args();dataset=load_json_dataset(args.dataset) if args.dataset else generate_fleet(args.vehicles,args.samples);report=DiagnosticAnalyzer(default_catalogue()).analyze(dataset,{"Powertrain.Motor.Vibration":{"threshold":3.0,"direction":"above"},"Powertrain.Motor.Temperature":{"threshold":100,"direction":"above"}});evidence=create_evidence(report);summary={"run_id":report["run_id"],"decision":report["decision"],"vehicles":report["dataset"]["vehicles"],"records":report["dataset"]["records"],"finding_count":report["finding_count"],"top_root_causes":report["root_causes"][:5],"top_priorities":report["priorities"][:5],"evidence_valid":verify_evidence(evidence)};text=json.dumps(summary,indent=2);print(text);Path(args.output).write_text(json.dumps(evidence,indent=2),encoding="utf-8") if args.output else None;return 0
if __name__=="__main__":raise SystemExit(main())
