"""Honest concurrency harness for API capacity measurements.

This measures the configured target only; it never infers or advertises a
supported capacity. Run against a deployed environment, not a developer laptop.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import time
from pathlib import Path

import httpx


async def run(base_url: str, connections: int, duration: float, path: str) -> dict:
    latencies: list[float] = []
    statuses: dict[str, int] = {}
    started = time.monotonic()
    limits = httpx.Limits(max_connections=connections, max_keepalive_connections=connections)
    async with httpx.AsyncClient(base_url=base_url, limits=limits, timeout=30) as client:
        async def one() -> None:
            while time.monotonic() - started < duration:
                begin = time.perf_counter()
                try:
                    response = await client.get(path)
                    status = str(response.status_code)
                except Exception as exc:
                    status = type(exc).__name__
                latencies.append((time.perf_counter() - begin) * 1000)
                statuses[status] = statuses.get(status, 0) + 1

        await asyncio.gather(*(one() for _ in range(connections)))
    elapsed = max(time.monotonic() - started, 0.001)
    ordered = sorted(latencies)
    percentile = lambda p: ordered[min(len(ordered) - 1, int(len(ordered) * p))] if ordered else None
    return {
        "target": base_url + path,
        "requested_concurrency": connections,
        "duration_seconds": duration,
        "requests": len(latencies),
        "requests_per_second": round(len(latencies) / elapsed, 2),
        "status_counts": statuses,
        "latency_ms": {
            "min": round(min(latencies), 2) if latencies else None,
            "mean": round(statistics.mean(latencies), 2) if latencies else None,
            "p50": round(percentile(0.50), 2) if latencies else None,
            "p95": round(percentile(0.95), 2) if latencies else None,
            "p99": round(percentile(0.99), 2) if latencies else None,
            "max": round(max(latencies), 2) if latencies else None,
        },
        "note": "Observed result for this run; not a capacity guarantee.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:8000")
    parser.add_argument("--connections", type=int, default=1000)
    parser.add_argument("--duration", type=float, default=30)
    parser.add_argument("--path", default="/api/v1/health")
    parser.add_argument("--report", default="load-reports/latest.json")
    args = parser.parse_args()
    if args.connections < 1 or args.connections > 10_000:
        parser.error("--connections must be between 1 and 10000")
    report = asyncio.run(run(args.url.rstrip("/"), args.connections, args.duration, args.path))
    destination = Path(args.report)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
