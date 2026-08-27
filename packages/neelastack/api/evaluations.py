import time

from fastapi import APIRouter, Depends, HTTPException

from packages.neelastack.auth.dependencies import current_user
from packages.neelastack.evaluations.metrics import exact_match
from packages.neelastack.evaluations.runner import EvaluationRunner

router = APIRouter(prefix="/evaluations", tags=["evaluations"])
_recent_results: list[dict] = []


@router.get("")
def evaluations():
    return {
        "status": "ready",
        "suites": ["quality", "safety", "latency", "cost", "rag"],
        "recent_runs": _recent_results[-20:],
    }


@router.post("/run")
async def run_evaluation(data: dict, user=Depends(current_user)):
    cases = data.get("cases", [])
    if not isinstance(cases, list) or not cases:
        raise HTTPException(status_code=422, detail="cases must be a non-empty list")
    if len(cases) > 100:
        raise HTTPException(status_code=422, detail="A maximum of 100 cases is supported")

    async def evaluate(value):
        # A deterministic baseline is useful offline and provides a smoke test
        # for datasets before connecting a model evaluator.
        return value

    started = time.perf_counter()
    rows = await EvaluationRunner().run_async(cases, evaluate)
    scored = [
        {**row, "score": exact_match(str(row["output"]), str(row["expected"]))}
        if row["expected"] is not None
        else {**row, "score": None}
        for row in rows
    ]
    scored_rows = [row for row in scored if row["score"] is not None]
    summary = {
        "count": len(scored),
        "mean_score": (
            round(sum(row["score"] for row in scored_rows) / len(scored_rows), 4)
            if scored_rows
            else None
        ),
        "latency_ms": round((time.perf_counter() - started) * 1000, 2),
    }
    result = {"id": len(_recent_results) + 1, "summary": summary, "results": scored}
    _recent_results.append(result)
    del _recent_results[:-20]
    return result
