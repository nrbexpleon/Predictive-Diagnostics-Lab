# Methods and limitations

- **Robust Z-score:** median and scaled MAD; fallback standard deviation for zero-MAD baselines.
- **EWMA:** detects sustained mean shifts with configured smoothing and standardized threshold.
- **CUSUM:** detects persistent positive or negative changes against the baseline mean and deviation.
- **Trend prognosis:** least-squares line projected to a configured threshold in sample units.
- **Cohorts:** variant, software version and operating cohort; unsuitable grouping can create misleading differences.
- **Root cause:** concentration of findings by version/variant/signal. Correlation is not causation.
- **Priority:** transparent severity × detector score × affected vehicles; it is not a maintenance order.

Production use requires data-quality controls, representative baselines, vehicle-specific thresholds, controlled false-positive/false-negative studies and qualified review.
