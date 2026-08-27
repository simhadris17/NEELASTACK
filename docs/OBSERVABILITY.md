# OBSERVABILITY

`GET /observability` reports request count, errors, average latency, telemetry
mode, and tracing mode. Authenticated `/observability/metrics` includes recent
request timings; `/observability/events` exposes the current user's audit
activity. Metrics are intentionally in-process and should be exported to a
shared collector for multi-instance deployments.
