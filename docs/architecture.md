# Architecture

1. **Domain:** typed telemetry, statistics, feature extraction, detectors, prognosis, cohorts, root-cause hypotheses, ranking and evidence.
2. **Ingestion:** JSON and CSV adapters convert external records to domain types.
3. **Application:** campaign execution, comparisons and bounded in-memory retention.
4. **Delivery:** standard-library CLI, HTTP API and browser console.

The analytical domain does not depend on a database, web framework, cloud platform or ML library. Future accelerated implementations must preserve the same evidence contracts and test against deterministic fixtures.

## Decision boundary

The lab only returns `eligible-for-human-review` or `investigation-required`. It does not issue maintenance commands, suppress DTCs, change vehicle configuration, or authorize OTA rollout.
