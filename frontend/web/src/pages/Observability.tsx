import { useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiGet } from "../api/workspace";

export default function Observability() {
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState("");
  async function load() { try { setData(await apiGet("/observability") as Record<string, unknown>); } catch (err) { setError(err instanceof Error ? err.message : "Unable to load metrics."); } }
  useEffect(() => { void load(); const timer = window.setInterval(() => void load(), 15000); return () => window.clearInterval(timer); }, []);
  return <WorkspacePage title="Observability" description="Monitor request health, latency and local telemetry." connected>
    <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">LIVE TELEMETRY</p><h2>System metrics</h2></div><button className="secondary-button" onClick={() => void load()}>Refresh</button></div>
      {error && <div className="error-banner" role="alert">{error}</div>}{!data ? <div className="state-card"><p>Loading metrics...</p></div> : <div className="workspace-data-list">{Object.entries(data).map(([key, value]) => <article className="workspace-data-card" key={key}><div className="workspace-data-field"><span>{key.replaceAll("_", " ")}</span><strong>{typeof value === "object" ? JSON.stringify(value, null, 2) : String(value)}</strong></div></article>)}</div>}
    </section>
  </WorkspacePage>;
}
