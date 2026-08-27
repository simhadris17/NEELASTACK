import { useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiGet } from "../api/workspace";

type Props = {
  title: string;
  description: string;
  endpoint: string;
  label: string;
};

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
          <pre
            style={{
              whiteSpace: "pre-wrap",
              overflowX: "auto",
              marginTop: "20px",
            }}
          >
            {JSON.stringify(data, null, 2)}
          </pre>
        )}
      </section>
    </WorkspacePage>
  );
}
