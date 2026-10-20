import unittest
from predictive_diagnostics.analyzer import DiagnosticAnalyzer
from predictive_diagnostics.cohorts import cohort_deviation,cohort_summary
from predictive_diagnostics.comparison import compare_reports
from predictive_diagnostics.config import default_catalogue
from predictive_diagnostics.evidence import create_evidence,sign_evidence,verify_evidence,verify_signed_evidence
from predictive_diagnostics.root_cause import correlate_findings
from predictive_diagnostics.synthetic import generate_fleet

class AnalyzerEvidenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.dataset=generate_fleet(20,20,42);cls.report=DiagnosticAnalyzer(default_catalogue()).analyze(cls.dataset,{"Powertrain.Motor.Vibration":{"threshold":3,"direction":"above"}})
 def test_synthetic_dimensions(self):self.assertEqual(len(self.dataset.records),400)
 def test_synthetic_reproducible(self):self.assertEqual(self.dataset.records,generate_fleet(20,20,42).records)
 def test_synthetic_bounds(self):
  with self.assertRaises(ValueError):generate_fleet(1,20)
 def test_report_vehicle_count(self):self.assertEqual(self.report["dataset"]["vehicles"],20)
 def test_report_has_findings(self):self.assertGreater(self.report["finding_count"],0)
 def test_report_requires_investigation(self):self.assertEqual(self.report["decision"],"investigation-required")
 def test_report_has_root_causes(self):self.assertTrue(self.report["root_causes"])
 def test_priorities_are_ordered(self):self.assertGreaterEqual(self.report["priorities"][0]["priority_score"],self.report["priorities"][-1]["priority_score"])
 def test_cohort_summary(self):self.assertTrue(cohort_summary(self.dataset.records,"Powertrain.Motor.Temperature"))
 def test_cohort_deviation(self):self.assertTrue(cohort_deviation(cohort_summary(self.dataset.records,"Powertrain.Motor.Temperature")))
 def test_root_cause_empty(self):self.assertEqual(correlate_findings([]),[])
 def test_evidence_verifies(self):self.assertTrue(verify_evidence(create_evidence(self.report)))
 def test_evidence_tampering_fails(self):
  evidence=create_evidence(self.report);evidence["report"]["decision"]="changed";self.assertFalse(verify_evidence(evidence))
 def test_signed_evidence_verifies(self):
  key=b"x"*32;self.assertTrue(verify_signed_evidence(sign_evidence(create_evidence(self.report),key),key))
 def test_short_key_rejected(self):
  with self.assertRaises(ValueError):sign_evidence(create_evidence(self.report),b"short")
 def test_comparison(self):
  candidate=dict(self.report);candidate["run_id"]="other";candidate["finding_count"]+=1;self.assertEqual(compare_reports(self.report,candidate)["finding_count_delta"],1)

if __name__=="__main__":unittest.main()
