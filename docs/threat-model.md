# Threat model

| Threat | Current control | Production work |
|---|---|---|
| Malformed/oversized telemetry | strict types, ranges, ordering and record/body bounds | JSON Schema, streaming validation, fuzzing |
| Fleet identity spoofing | required vehicle/version/variant fields | authenticated vehicle identity and certificates |
| Data poisoning | explainable baselines and evidence hash | signed telemetry, trusted data lake, lineage review |
| Misleading root-cause claim | explicit hypothesis wording and concentration evidence | causal experiments and controlled cohorts |
| Evidence tampering | canonical SHA-256 and optional HMAC | KMS/HSM signatures, trusted timestamp, immutable store |
| Unauthorized API | loopback default and optional bearer token | OIDC, RBAC, tenant isolation, audit |
| Sensitive fleet disclosure | synthetic public fixture | encryption, retention, redaction, aggregation thresholds |
| Unsafe action | no maintenance/vehicle write API | independent workflow approval and safety integration |
| Resource exhaustion | request/record/run bounds | rate limits and isolated workers |

Never commit VINs, production telemetry, customer identifiers, credentials, thresholds or signing keys.
