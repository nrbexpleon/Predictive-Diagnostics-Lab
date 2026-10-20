import unittest
from predictive_diagnostics.models import AnalysisPolicy,SignalDefinition,TelemetryDataset,TelemetryRecord
from predictive_diagnostics.statistics import correlation,linear_regression,mad,mean,percentile,stdev,variance

class ModelsStatisticsTests(unittest.TestCase):
 def setUp(self):self.signal=SignalDefinition("speed","km/h",0,300);self.catalogue={"speed":self.signal};self.records=(TelemetryRecord("v",0,"1","a",{"speed":1}),TelemetryRecord("v",1,"1","a",{"speed":2}))
 def test_signal_accepts_range(self):self.signal.validate(20)
 def test_signal_rejects_range(self):
  with self.assertRaises(ValueError):self.signal.validate(301)
 def test_signal_rejects_nan(self):
  with self.assertRaises(ValueError):self.signal.validate(float("nan"))
 def test_dataset_validates(self):TelemetryDataset("d","1",self.records).validate(self.catalogue)
 def test_dataset_rejects_unknown_signal(self):
  records=(self.records[0],TelemetryRecord("v",1,"1","a",{"x":1}))
  with self.assertRaises(ValueError):TelemetryDataset("d","1",records).validate(self.catalogue)
 def test_dataset_rejects_time_order(self):
  records=(self.records[0],TelemetryRecord("v",0,"1","a",{"speed":2}))
  with self.assertRaises(ValueError):TelemetryDataset("d","1",records).validate(self.catalogue)
 def test_dataset_rejects_too_small(self):
  with self.assertRaises(ValueError):TelemetryDataset("d","1",self.records[:1]).validate(self.catalogue)
 def test_policy_validates(self):AnalysisPolicy().validate()
 def test_policy_rejects_fraction(self):
  with self.assertRaises(ValueError):AnalysisPolicy(baseline_fraction=.9).validate()
 def test_mean(self):self.assertEqual(mean([1,2,3]),2)
 def test_variance(self):self.assertEqual(variance([1,2,3]),1)
 def test_stdev(self):self.assertEqual(stdev([1,2,3]),1)
 def test_mad(self):self.assertEqual(mad([1,2,100]),1)
 def test_percentile(self):self.assertEqual(percentile([1,2,3,4],.95),4)
 def test_regression(self):self.assertEqual(linear_regression([(0,1),(1,3)])[0],2)
 def test_correlation(self):self.assertAlmostEqual(correlation([1,2,3],[2,4,6]),1)

if __name__=="__main__":unittest.main()
