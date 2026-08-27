# EVALUATIONS

`GET /evaluations` lists the built-in quality, safety, latency, cost, and RAG
suites. Authenticated `POST /evaluations/run` runs up to 100 deterministic
cases, returning exact-match scores and latency. This offline baseline is
designed to be replaced or extended with model-backed evaluators.
