import { FormEvent, useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiGet, apiPost } from "../api/workspace";

type Evaluation = { id: number; summary: { count: number; mean_score: number | null; latency_ms: number }; results: Array<{ input: unknown; score: number | null }> };
export default function Evaluations() {
  const [status, setStatus] = useState<{ suites?: string[]; recent_runs?: Evaluation[] }>({});
  const [cases, setCases] = useState('[{"input":"hello","expected":"hello"}]');
  const [result, setResult] = useState<Evaluation | null>(null);
  const [error, setError] = useState("");
  async function load() { try { setStatus(await apiGet("/evaluations") as typeof status); } catch (err) { setError(err instanceof Error ? err.message : "Unable to load evaluations."); } }
  useEffect(() => { void load(); }, []);
  async function run(event: FormEvent) {
    event.preventDefault(); setError("");
    try { const parsed = JSON.parse(cases); if (!Array.isArray(parsed)) throw new Error("Cases must be an array"); setResult(await apiPost("/evaluations/run", { cases: parsed }) as Evaluation); await load(); }
    catch (err) { setError(err instanceof Error ? err.message : "Evaluation failed."); }
  }
  return <WorkspacePage title="Evaluations" description="Run deterministic quality checks and inspect latency results." connected>
    <div className="workspace-grid"><section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">TEST SUITES</p><h2>Available suites</h2></div></div><div className="workspace-data-list">{(status.suites || []).map((suite) => <article className="workspace-data-card" key={suite}><strong>{suite}</strong><span className="project-status">READY</span></article>)}</div></section>
      <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">OFFLINE RUNNER</p><h2>Run cases</h2></div></div><form className="project-form" onSubmit={run}><label htmlFor="evaluation-cases">Cases JSON</label><textarea id="evaluation-cases" rows={6} value={cases} onChange={(e) => setCases(e.target.value)} /><button className="primary-button">Run evaluation</button></form></section></div>
    {error && <div className="error-banner" role="alert">{error}</div>}
    {result && <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">LATEST RESULT</p><h2>Score {result.summary.mean_score ?? "—"}</h2></div></div><p className="card-description">{result.summary.count} cases · {result.summary.latency_ms} ms</p><pre className="workspace-raw-value">{JSON.stringify(result.results, null, 2)}</pre></section>}
  </WorkspacePage>;
}
