# Load testing

Run the harness against the exact deployment configuration being evaluated:

```powershell
python tests/load/run_load_test.py --url https://api.example.com --connections 1000 --duration 60
```

The JSON report records observed throughput, status codes, and latency
percentiles. It intentionally does **not** claim that the service supports
1000 concurrent connections. Repeat from a dedicated load generator and
compare reports after each deployment. The endpoint is unauthenticated health;
authenticated and provider-backed workloads must be measured separately.
