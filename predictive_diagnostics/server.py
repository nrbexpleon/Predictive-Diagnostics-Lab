from __future__ import annotations
import json,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .analyzer import DiagnosticAnalyzer
from .comparison import compare_reports
from .config import default_catalogue,policy_from_dict
from .evidence import create_evidence,verify_evidence
from .io import dataset_from_dict
from .synthetic import generate_fleet

REPORTS:dict[str,dict]={};MAX_BODY=10_000_000;ROOT=Path(__file__).resolve().parent.parent
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.security();path=urlparse(self.path).path
        if path.startswith("/api/") and not self.authorized():return self.send_json(401,{"error":"unauthorized"})
        if path=="/api/health":return self.send_json(200,{"status":"healthy","version":"0.1.0"})
        if path=="/api/example":
            dataset=generate_fleet(20,20);return self.send_json(200,{"name":dataset.name,"version":dataset.version,"records":[{"vehicle_id":r.vehicle_id,"timestamp_ms":r.timestamp_ms,"software_version":r.software_version,"variant":r.variant,"values":r.values,"trip_id":r.trip_id,"cohort":r.cohort} for r in dataset.records]})
        if path.startswith("/api/analyses/"):
            parts=path.strip("/").split("/");report=REPORTS.get(parts[2])
            if report is None:return self.send_json(404,{"error":"not-found"})
            return self.send_json(200,create_evidence(report) if len(parts)>3 and parts[3]=="evidence" else report)
        files={"/":"index.html","/index.html":"index.html","/app.js":"app.js","/styles.css":"styles.css"}
        if path in files:return self.send_file(ROOT/"public"/files[path])
        self.send_json(404,{"error":"not-found"})
    def do_POST(self):
        self.security();path=urlparse(self.path).path
        if path.startswith("/api/") and not self.authorized():return self.send_json(401,{"error":"unauthorized"})
        try:payload=self.body()
        except (ValueError,json.JSONDecodeError) as error:return self.send_json(400,{"error":str(error)})
        try:
            if path=="/api/analyses":
                dataset=dataset_from_dict(payload["dataset"]);policy=policy_from_dict(payload.get("policy",{}));report=DiagnosticAnalyzer(default_catalogue(),policy).analyze(dataset,payload.get("thresholds"));REPORTS[report["run_id"]]=report
                while len(REPORTS)>100:REPORTS.pop(next(iter(REPORTS)))
                return self.send_json(201,report)
            if path=="/api/evidence/verify":return self.send_json(200,{"valid":verify_evidence(payload)})
            if path=="/api/compare":return self.send_json(200,compare_reports(REPORTS[payload["baseline_run_id"]],REPORTS[payload["candidate_run_id"]]))
            return self.send_json(404,{"error":"not-found"})
        except (ValueError,KeyError,TypeError) as error:return self.send_json(400,{"error":str(error)})
    def authorized(self)->bool:
        token=os.getenv("API_TOKEN");return not token or self.headers.get("Authorization")==f"Bearer {token}"
    def body(self)->dict:
        length=int(self.headers.get("Content-Length","0"));
        if length>MAX_BODY:raise ValueError("body-too-large")
        return json.loads(self.rfile.read(length))
    def security(self):
        pass
    def send_json(self,status:int,value:dict):
        data=json.dumps(value,separators=(",",":")).encode();self.send_response(status);self.send_header("Content-Type","application/json; charset=utf-8");self.common_headers();self.send_header("Content-Length",str(len(data)));self.end_headers();self.wfile.write(data)
    def send_file(self,path:Path):
        data=path.read_bytes();content={".html":"text/html; charset=utf-8",".js":"text/javascript; charset=utf-8",".css":"text/css; charset=utf-8"}[path.suffix];self.send_response(200);self.send_header("Content-Type",content);self.common_headers();self.send_header("Content-Length",str(len(data)));self.end_headers();self.wfile.write(data)
    def common_headers(self):
        self.send_header("Cache-Control","no-store");self.send_header("X-Content-Type-Options","nosniff");self.send_header("Referrer-Policy","no-referrer");self.send_header("Content-Security-Policy","default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
    def log_message(self,format,*args):return

def main():
    port=int(os.getenv("PORT","8084"));server=ThreadingHTTPServer(("127.0.0.1",port),Handler);print(f"Predictive Diagnostics Lab listening on http://127.0.0.1:{port}");server.serve_forever()
if __name__=="__main__":main()
