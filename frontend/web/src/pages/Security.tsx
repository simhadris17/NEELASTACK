import { useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiGet } from "../api/workspace";

type AuditEvent = { id: number; event_type: string; resource_type?: string; resource_id?: string; created_at?: string };
export default function Security() {
  const [status, setStatus] = useState<Record<string, unknown> | null>(null);
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [error, setError] = useState("");
  async function load() {
    try {
      const [security, audit] = await Promise.all([apiGet("/security"), apiGet("/security/audit")]);
      setStatus(security as Record<string, unknown>); setEvents((audit as { events?: AuditEvent[] }).events || []);
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to load security status."); }
  }
  useEffect(() => { void load(); }, []);
  return <WorkspacePage title="Security" description="Review authentication, rate limits and audit activity." connected>
    {error && <div className="error-banner" role="alert">{error}</div>}<div className="workspace-grid"><section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">CONTROL PLANE</p><h2>Security status</h2></div><button className="secondary-button" onClick={() => void load()}>Refresh</button></div>{status && <div className="workspace-data-list">{Object.entries(status).map(([key, value]) => <article className="workspace-data-card" key={key}><div className="workspace-data-field"><span>{key.replaceAll("_", " ")}</span><strong>{typeof value === "object" ? JSON.stringify(value) : String(value)}</strong></div></article>)}</div>}</section>
      <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">AUDIT LOG</p><h2>Recent events</h2></div></div>{events.length === 0 ? <div className="state-card"><p>No audit events yet.</p></div> : <div className="workspace-data-list">{events.map((event) => <article className="workspace-data-card" key={event.id}><div className="workspace-data-field"><span>event</span><strong>{event.event_type}</strong></div><div className="workspace-data-field"><span>resource</span><strong>{event.resource_type || "—"} {event.resource_id || ""}</strong></div></article>)}</div>}</section></div>
  </WorkspacePage>;
}
