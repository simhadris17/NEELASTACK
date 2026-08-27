import { FormEvent, ReactNode, useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiDelete, apiGet, apiPost } from "../api/workspace";

type Agent = { id: number; name: string; config_json: string };
type AgentRunResult = {
  response?: string;
  plan?: string;
  research?: string;
  implementation?: string;
  execution?: string;
  review?: string;
};
type ConversationMessage = { role: "user" | "assistant"; content: string };

function renderTextBlock(text: string, keyPrefix: string): ReactNode[] {
  return text.split("\n").map((line, index) => {
    const key = `${keyPrefix}-line-${index}`;
    if (/^\s*[A-Za-z+#.-]+Copy\s*$/.test(line)) return <span key={key} />;
    if (!line.trim()) return <div className="agent-markdown-spacer" key={key} />;
    if (line.startsWith("### ")) return <h4 key={key}>{line.slice(4)}</h4>;
    if (line.startsWith("## ")) return <h3 key={key}>{line.slice(3)}</h3>;
    if (line.startsWith("# ")) return <h2 key={key}>{line.slice(2)}</h2>;
    if (/^\s*[-*]\s+/.test(line)) {
      return <li key={key}>{line.replace(/^\s*[-*]\s+/, "")}</li>;
    }
    if (/^\s*\d+\.\s+/.test(line)) {
      return <li key={key}>{line.replace(/^\s*\d+\.\s+/, "")}</li>;
    }
    return <p key={key}>{line}</p>;
  });
}

function AgentMarkdown({ content }: { content: string }) {
  const parts = content.split(/```([^\n]*)\n([\s\S]*?)```/g);
  const nodes: ReactNode[] = [];
  for (let index = 0; index < parts.length; index += 3) {
    const text = parts[index];
    if (text) nodes.push(...renderTextBlock(text, `text-${index}`));
    const language = parts[index + 1]?.replace(/Copy$/, "");
    const code = parts[index + 2];
    if (code !== undefined) {
      nodes.push(
        <div className="agent-code-block" key={`code-${index}`}>
          <div className="agent-code-header">
            <span>{language.trim() || "code"}</span>
            <button
              type="button"
              onClick={() => void navigator.clipboard.writeText(code.trim())}
            >
              Copy
            </button>
          </div>
          <pre><code>{code.trim()}</code></pre>
        </div>,
      );
    }
  }
  return <div className="agent-markdown">{nodes}</div>;
}

export default function Agents() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [name, setName] = useState("");
  const [goal, setGoal] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<AgentRunResult | null>(null);
  const [conversation, setConversation] = useState<ConversationMessage[]>(() => {
    try {
      const saved = localStorage.getItem("neelastack_agent_conversation");
      return saved ? (JSON.parse(saved) as ConversationMessage[]) : [];
    } catch {
      return [];
    }
  });

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = (await apiGet("/agents")) as { agents?: Agent[] };
      setAgents(data.agents || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load agents.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { void load(); }, []);
  useEffect(() => {
    localStorage.setItem(
      "neelastack_agent_conversation",
      JSON.stringify(conversation.slice(-12)),
    );
  }, [conversation]);

  async function create(event: FormEvent) {
    event.preventDefault();
    if (!name.trim()) return;
    setBusy(true);
    setError("");
    try {
      const agent = (await apiPost("/agents", { name: name.trim() })) as Agent;
      setAgents((current) => [agent, ...current]);
      setName("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to create agent.");
    } finally {
      setBusy(false);
    }
  }

  async function run(event: FormEvent) {
    event.preventDefault();
    if (!goal.trim()) return;
    setBusy(true);
    setError("");
    setResult(null);
    try {
      const token = localStorage.getItem("neelastack_token") || "";
      const response = await fetch("http://127.0.0.1:8000/agents/run/stream", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          goal: goal.trim(),
          history: conversation.slice(-8),
        }),
      });
      if (!response.ok || !response.body) {
        const text = await response.text();
        throw new Error(text || `Agent request failed: ${response.status}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let answer = "";
      setResult({ response: "" });
      while (true) {
        const chunk = await reader.read();
        if (chunk.done) break;
        answer += decoder.decode(chunk.value, { stream: true });
        setResult({ response: answer });
      }
      answer += decoder.decode();
      setResult({ response: answer });
      setConversation((current) => [
        ...current,
        { role: "user", content: goal.trim() },
        { role: "assistant", content: answer },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to run agent.");
    } finally {
      setBusy(false);
    }
  }

  async function remove(id: number) {
    try {
      await apiDelete(`/agents/${id}`);
      setAgents((current) => current.filter((agent) => agent.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to delete agent.");
    }
  }

  return (
    <WorkspacePage title="Agents" description="Create, manage and run AI agents inside the active project workspace." connected>
      <div className="workspace-grid">
        <section className="workspace-card create-card">
          <div className="card-heading"><div><p className="card-kicker">NEW AGENT</p><h2>Create an agent</h2></div><div className="card-icon">◎</div></div>
          <p className="card-description">Add an AI agent to this workspace.</p>
          <form onSubmit={create} className="project-form">
            <label htmlFor="agent-name">Agent name</label>
            <input id="agent-name" value={name} onChange={(event) => setName(event.target.value)} placeholder="e.g. Research Assistant" disabled={busy} />
            <button className="primary-button" type="submit" disabled={busy || !name.trim()}>{busy ? "Creating..." : "Create agent"}</button>
          </form>
        </section>
        <section className="workspace-card">
          <div className="card-heading"><div><p className="card-kicker">AGENT RUNNER</p><h2>Ask an agent</h2></div></div>
          <form onSubmit={run} className="project-form">
            <label htmlFor="agent-goal">Goal</label>
            <textarea id="agent-goal" value={goal} onChange={(event) => setGoal(event.target.value)} placeholder="e.g. Plan a calculator project" rows={3} disabled={busy} />
            <button className="primary-button" type="submit" disabled={busy || !goal.trim()}>{busy ? "Running..." : "Run agent"}</button>
          </form>
          {conversation.length > 0 && (
            <div className="agent-conversation">
              {conversation.map((message, index) => (
                <article className={`agent-message ${message.role}`} key={`${message.role}-${index}`}>
                  <p className="card-kicker">{message.role === "user" ? "YOU" : "NEELASTACK"}</p>
                  {message.role === "assistant" ? (
                    <AgentMarkdown content={message.content} />
                  ) : (
                    <p>{message.content}</p>
                  )}
                </article>
              ))}
            </div>
          )}
          {busy && result?.response && (
            <div className="agent-result">
              <article className="agent-result-section">
                <p className="card-kicker">NEELASTACK</p>
                <AgentMarkdown content={result.response} />
              </article>
            </div>
          )}
        </section>
      </div>
      <section className="workspace-card">
        <div className="card-heading"><div><p className="card-kicker">LIVE BACKEND</p><h2>Registered Agents</h2></div><button className="secondary-button" type="button" onClick={() => void load()} disabled={loading}>{loading ? "Refreshing..." : "Refresh"}</button></div>
        {error && <div className="error-banner" role="alert">{error}</div>}
        {loading ? <div className="state-card"><p>Loading agents...</p></div> : agents.length === 0 ? <div className="state-card"><div className="empty-icon">◎</div><h3>No agents yet</h3><p>Create your first agent above.</p></div> : <div className="project-list">{agents.map((agent) => <article className="project-row" key={agent.id}><div className="project-mark">◎</div><div className="project-info"><h3>{agent.name}</h3><p>Agent #{agent.id} · Ready</p></div><button className="secondary-button" type="button" onClick={() => void remove(agent.id)}>Delete</button></article>)}</div>}
      </section>
    </WorkspacePage>
  );
}
