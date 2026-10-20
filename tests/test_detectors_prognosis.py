import unittest
from predictive_diagnostics.detectors import cusum,ewma,robust_zscore
from predictive_diagnostics.features import window_features
from predictive_diagnostics.prognosis import remaining_useful_samples

class DetectorPrognosisTests(unittest.TestCase):
 def test_robust_z_detects_outlier(self):self.assertTrue(robust_zscore([1,1,1,10],3,3))
 def test_robust_z_ignores_normal(self):self.assertFalse(robust_zscore([1,1,1,1],3,3))
 def test_ewma_detects_shift(self):self.assertTrue(ewma([1,1,1,5,5,5],3,.5,2))
 def test_ewma_ignores_flat(self):self.assertFalse(ewma([1,1,1,1],2,.5,3))
 def test_cusum_detects_sustained_shift(self):self.assertTrue(cusum([1,1,1,3,3,3,3],3,.2,2))
 def test_cusum_ignores_baseline(self):self.assertFalse(cusum([1,1,1,1],2,.5,5))
 def test_features_count(self):self.assertEqual(window_features([1,2,3],[0,1,2])["count"],3)
 def test_features_slope(self):self.assertEqual(window_features([1,2,3],[0,1,2])["slope_per_ms"],1)
 def test_features_reject_shape(self):
  with self.assertRaises(ValueError):window_features([1],[0,1])
 def test_prognosis_above(self):self.assertAlmostEqual(remaining_useful_samples([1,2,3,4],10).remaining_samples,6)
 def test_prognosis_not_approaching(self):self.assertIsNone(remaining_useful_samples([4,3,2,1],10).remaining_samples)
 def test_prognosis_insufficient(self):self.assertEqual(remaining_useful_samples([1,2],10).confidence,"insufficient-data")

if __name__=="__main__":unittest.main()
