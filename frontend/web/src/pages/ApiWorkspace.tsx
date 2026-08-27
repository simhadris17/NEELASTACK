import { useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiGet } from "../api/workspace";

type Props = {
  title: string;
  description: string;
  endpoint: string;
  label: string;
};

function displayValue(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return JSON.stringify(value, null, 2);
}

function WorkspaceData({ data, label }: { data: unknown; label: string }) {
  if (Array.isArray(data)) {
    if (data.length === 0) {
      return (
        <div className="state-card">
          <div className="empty-icon">◎</div>
          <h3>No {label.toLowerCase()} yet</h3>
          <p>Data created in this workspace will appear here.</p>
        </div>
      );
    }

    return (
      <div className="workspace-data-list">
        {data.map((item, index) => (
          <article className="workspace-data-card" key={`${label}-${index}`}>
            {typeof item === "object" && item !== null ? (
              Object.entries(item).map(([key, value]) => (
                <div className="workspace-data-field" key={key}>
                  <span>{key.replaceAll("_", " ")}</span>
                  <strong>{displayValue(value)}</strong>
                </div>
              ))
            ) : (
              <strong>{displayValue(item)}</strong>
            )}
          </article>
        ))}
      </div>
    );
  }

  if (typeof data === "object" && data !== null) {
    const entries = Object.entries(data);
    return (
      <div className="workspace-data-list">
        {entries.map(([key, value]) => (
          <article className="workspace-data-card" key={key}>
            <div className="workspace-data-field">
              <span>{key.replaceAll("_", " ")}</span>
              <strong>{displayValue(value)}</strong>
            </div>
          </article>
        ))}
      </div>
    );
  }

  return <pre className="workspace-raw-value">{displayValue(data)}</pre>;
}

export default function ApiWorkspace({
  title,
  description,
  endpoint,
  label,
}: Props) {
  const [data, setData] = useState<unknown>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");

    try {
      const result = await apiGet(endpoint);
      setData(result);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to load workspace.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
  }, [endpoint]);

  return (
    <WorkspacePage
      title={title}
      description={description}
      connected
    >
      <section className="workspace-card">
        <div className="card-heading">
          <div>
            <p className="card-kicker">LIVE BACKEND</p>
            <h2>{label}</h2>
          </div>

          <button
            className="secondary-button"
            type="button"
            onClick={() => void load()}
            disabled={loading}
          >
            {loading ? "Refreshing..." : "Refresh"}
          </button>
        </div>

        {error ? (
          <div className="error-banner" role="alert">
            {error}
          </div>
        ) : loading ? (
          <div className="state-card">
            <div className="loading-pulse" />
            <p>Loading from NEELASTACK backend...</p>
          </div>
        ) : (
          <WorkspaceData data={data} label={label} />
        )}
      </section>
    </WorkspacePage>
  );
}
