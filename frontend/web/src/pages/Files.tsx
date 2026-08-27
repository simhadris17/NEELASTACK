import { FormEvent, useEffect, useState } from "react";
import WorkspacePage from "../components/WorkspacePage";
import { apiDelete, apiGet, apiUpload } from "../api/workspace";

type FileItem = { id: number; name: string; size: number; preview: string };

export default function Files() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<FileItem[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    const data = (await apiGet("/files")) as { files?: FileItem[] };
    setFiles(data.files || []);
  }

  useEffect(() => { void load().catch((err) => setError(String(err))); }, []);

  async function upload(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const input = event.currentTarget.elements.namedItem("file");
    if (!(input instanceof HTMLInputElement) || !input.files?.[0]) return;
    setBusy(true);
    setError("");
    try {
      await apiUpload("/files/upload", input.files[0]);
      event.currentTarget.reset();
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally { setBusy(false); }
  }

  async function search(event: FormEvent) {
    event.preventDefault();
    if (!query.trim()) { setResults([]); return; }
    try {
      const data = (await apiGet(`/rag/search?q=${encodeURIComponent(query.trim())}`)) as { results?: FileItem[] };
      setResults(data.results || []);
    } catch (err) { setError(err instanceof Error ? err.message : "Search failed"); }
  }

  async function remove(id: number) {
    await apiDelete(`/files/${id}`);
    setFiles((current) => current.filter((file) => file.id !== id));
  }

  return (
    <WorkspacePage title="Files" description="Upload and search project knowledge sources." connected>
      <div className="workspace-grid">
        <section className="workspace-card">
          <div className="card-heading"><div><p className="card-kicker">KNOWLEDGE BASE</p><h2>Upload a file</h2></div></div>
          <p className="card-description">UTF-8 text files up to 2 MB are indexed privately to your account.</p>
          <form className="project-form" onSubmit={upload}>
            <input name="file" type="file" accept=".txt,.md,.json,.csv,.py,.ts,.tsx" disabled={busy} />
            <button className="primary-button" type="submit" disabled={busy}>{busy ? "Uploading..." : "Upload and index"}</button>
          </form>
        </section>
        <section className="workspace-card">
          <div className="card-heading"><div><p className="card-kicker">RAG SEARCH</p><h2>Search knowledge</h2></div></div>
          <form className="project-form" onSubmit={search}>
            <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search files..." />
            <button className="secondary-button" type="submit">Search</button>
          </form>
        </section>
      </div>
      {error && <div className="error-banner" role="alert">{error}</div>}
      <section className="workspace-card">
        <div className="card-heading"><div><p className="card-kicker">LIVE BACKEND</p><h2>{results.length ? "Search results" : "Indexed files"}</h2></div></div>
        <div className="workspace-data-list">
          {(results.length ? results : files).map((file) => (
            <article className="workspace-data-card" key={file.id}>
              <div className="workspace-data-field"><span>name</span><strong>{file.name}</strong></div>
              <div className="workspace-data-field"><span>size</span><strong>{file.size.toLocaleString()} bytes</strong></div>
              <div className="workspace-data-field"><span>preview</span><strong>{file.preview}</strong></div>
              {!results.length && <button className="secondary-button" type="button" onClick={() => void remove(file.id)}>Delete</button>}
            </article>
          ))}
          {!(results.length ? results : files).length && <div className="state-card"><h3>No files yet</h3><p>Upload a document to start building project memory.</p></div>}
        </div>
      </section>
    </WorkspacePage>
  );
}
