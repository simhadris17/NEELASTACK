import inspect
import time


class EvaluationRunner:
    """Run deterministic evaluation cases without requiring a hosted evaluator."""

    async def run_async(self, cases, fn):
        results = []
        for case in cases:
            value = case.get("input", case) if isinstance(case, dict) else case
            started = time.perf_counter()
            output = fn(value)
            if inspect.isawaitable(output):
                output = await output
            results.append(
                {
                    "input": value,
                    "expected": case.get("expected") if isinstance(case, dict) else None,
                    "output": output,
                    "latency_ms": round((time.perf_counter() - started) * 1000, 2),
                }
            )
        return results

    def run(self, cases, fn):
        return [{"input": c, "output": fn(c)} for c in cases]
