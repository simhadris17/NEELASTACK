import { FormEvent, useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiGet, apiPost } from "../api/workspace";

type Tool = { id?: number; name: string; tool_type?: string; config?: Record<string, unknown> };

export default function MCP() {
  const [tools, setTools] = useState<Tool[]>([]);
  const [name, setName] = useState("");
  const [args, setArgs] = useState("{}");
  const [selected, setSelected] = useState("");
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try {
      const data = await apiGet("/mcp/tools") as { tools?: string[]; db_tools?: Tool[] };
      setTools([...(data.tools || []).map((item) => ({ name: item, tool_type: "builtin" })), ...(data.db_tools || [])]);
    } catch (err) { setError(err instanceof Error ? err.message : "Unable to load MCP tools."); }
  }
  useEffect(() => { void load(); }, []);
  async function execute(event: FormEvent) {
    event.preventDefault(); setError(""); setResult("");
    try { const data = await apiPost("/mcp/execute", { name: selected, args: JSON.parse(args) }); setResult(JSON.stringify(data.result, null, 2)); }
    catch (err) { setError(err instanceof Error ? err.message : "Tool execution failed."); }
  }
  async function register(event: FormEvent) {
    event.preventDefault(); setError("");
    try { await apiPost("/mcp/tools", { name, tool_type: "describe_code_task", config: {} }); setName(""); await load(); }
    catch (err) { setError(err instanceof Error ? err.message : "Unable to register tool."); }
  }
  return <WorkspacePage title="MCP" description="Inspect and safely execute registered Model Context Protocol tools." connected>
    <div className="workspace-grid">
      <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">TOOL REGISTRY</p><h2>{tools.length} available tools</h2></div><button className="secondary-button" onClick={() => void load()}>Refresh</button></div>
        {tools.length === 0 ? <div className="state-card"><p>No tools registered.</p></div> : <div className="workspace-data-list">{tools.map((tool) => <article className="workspace-data-card" key={`${tool.name}-${tool.id || "builtin"}`}><div className="workspace-data-field"><span>name</span><strong>{tool.name}</strong></div><div className="workspace-data-field"><span>type</span><strong>{tool.tool_type}</strong></div><button className="secondary-button" onClick={() => setSelected(tool.name)}>Use tool</button></article>)}</div>}
      </section>
      <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">EXECUTION</p><h2>Run a tool</h2></div></div>
        <form className="project-form" onSubmit={execute}><label htmlFor="mcp-tool">Tool name</label><input id="mcp-tool" value={selected} onChange={(e) => setSelected(e.target.value)} placeholder="describe_code_task" required /><label htmlFor="mcp-args">Arguments JSON</label><textarea id="mcp-args" rows={4} value={args} onChange={(e) => setArgs(e.target.value)} /><button className="primary-button">Execute</button></form>
        {result && <pre className="workspace-raw-value">{result}</pre>}
      </section>
    </div>
    <section className="workspace-card"><div className="card-heading"><div><p className="card-kicker">LOCAL REGISTRY</p><h2>Register code tool</h2></div></div><form className="project-form" onSubmit={register}><input value={name} onChange={(e) => setName(e.target.value)} placeholder="Tool name" required /><button className="secondary-button">Register</button></form></section>
    {error && <div className="error-banner" role="alert">{error}</div>}
  </WorkspacePage>;
}
