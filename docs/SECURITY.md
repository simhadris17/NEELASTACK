# SECURITY

Authentication uses JWT bearer tokens and all workspace resources are
user-scoped. The API adds security headers, an in-process rate limiter (configure
`RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW_SECONDS`), and audit records for
authentication, file, workflow, and MCP actions. `/security/audit` is
authenticated. For multiple API workers, replace the in-process limiter with a
shared Redis implementation.
