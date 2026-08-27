import { FormEvent, useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiDelete, apiGet, apiPost } from "../api/workspace";

type Workflow = { id: number; name: string; definition_json: string; created_at?: string };
type Run = { id: number; status: string; output_json?: string; error?: string | null; created_at?: string };

export default function Workflows() {
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [runs, setRuns] = useState<Run[]>([]);
  const [name, setName] = useState("");
  const [definition, setDefinition] = useState('{"steps":["collect","analyze"]}');
  const [selected, setSelected] = useState<number | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    try {
      const data = await apiGet("/workflows") as { workflows: Workflow[] };
      setWorkflows(data.workflows || []);
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to load workflows."); }
  }
  async function loadRuns(id: number) {
    setSelected(id);
    try {
      const data = await apiGet(`/workflows/${id}/runs`) as { runs: Run[] };
      setRuns(data.runs || []);
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to load runs."); }
  }
  useEffect(() => { void load(); }, []);

  async function create(event: FormEvent) {
    event.preventDefault(); setBusy(true); setError("");
    try {
      JSON.parse(definition);
      await apiPost("/workflows", { name, definition_json: definition });
      setName(""); await load();
    } catch (err) { setError(err instanceof Error ? err.message : "Invalid workflow definition."); }
    finally { setBusy(false); }
  }
  async function run(id: number) {
    setBusy(true); setError("");
    try { await apiPost(`/workflows/${id}/run`, { input: {} }); await loadRuns(id); }
    catch (err) { setError(err instanceof Error ? err.message : "Workflow run failed."); }
    finally { setBusy(false); }
  }
  async function remove(id: number) {
    try { await apiDelete(`/workflows/${id}`); setWorkflows((items) => items.filter((item) => item.id !== id)); }
    catch (err) { setError(err instanceof Error ? err.message : "Unable to delete workflow."); }
  }

  return (
    <WorkspacePage title="Workflows" description="Build, run and monitor multi-step automations." connected>
      <div className="workspace-grid">
        <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">NEW WORKFLOW</p><h2>Create workflow</h2></div></div>
          <form className="project-form" onSubmit={create}><label htmlFor="workflow-name">Name</label><input id="workflow-name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Research pipeline" required />
            <label htmlFor="workflow-definition">Definition JSON</label><textarea id="workflow-definition" rows={5} value={definition} onChange={(e) => setDefinition(e.target.value)} />
            <button className="primary-button" disabled={busy}>{busy ? "Working..." : "Create workflow"}</button></form>
        </section>
        <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">RUN HISTORY</p><h2>{selected ? `Workflow #${selected}` : "Select a workflow"}</h2></div></div>
          {!selected ? <div className="state-card"><p>Choose Run history on a workflow.</p></div> : runs.length === 0 ? <div className="state-card"><p>No runs yet.</p></div> :
            <div className="workspace-data-list">{runs.map((item) => <article className="workspace-data-card" key={item.id}><div className="workspace-data-field"><span>run</span><strong>#{item.id} · {item.status}</strong></div><div className="workspace-data-field"><span>output</span><strong>{item.error || item.output_json || "—"}</strong></div></article>)}</div>}
        </section>
      </div>
      {error && <div className="error-banner" role="alert">{error}</div>}
      <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">LIVE BACKEND</p><h2>Available workflows</h2></div><button className="secondary-button" onClick={() => void load()}>Refresh</button></div>
        {workflows.length === 0 ? <div className="state-card"><p>No workflows yet.</p></div> : <div className="workspace-data-list">{workflows.map((item) => <article className="workspace-data-card" key={item.id}><div className="workspace-data-field"><span>name</span><strong>{item.name}</strong></div><div className="workspace-data-field"><span>definition</span><strong>{item.definition_json}</strong></div><div className="workspace-actions"><button className="primary-button" disabled={busy} onClick={() => void run(item.id)}>Run now</button><button className="secondary-button" onClick={() => void loadRuns(item.id)}>Run history</button><button className="secondary-button" onClick={() => void remove(item.id)}>Delete</button></div></article>)}</div>}
      </section>
    </WorkspacePage>
  );
}
