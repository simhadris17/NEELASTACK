import { useState } from "react";
import { useNavigate } from "react-router-dom";
import WorkspacePage from "../components/WorkspacePage";
import { getToken, logout } from "../services/auth";

export default function Settings() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function deleteAccount() {
    if (!window.confirm("Delete your account and all workspace data permanently?")) return;
    setBusy(true);
    setError("");
    try {
      const response = await fetch("http://127.0.0.1:8000/auth/account", {
        method: "DELETE",
        headers: { Authorization: `Bearer ${getToken() || ""}` },
      });
      if (!response.ok) throw new Error((await response.json()).detail || "Account deletion failed");
      logout();
      navigate("/register", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Account deletion failed");
      setBusy(false);
    }
  }

  return (
    <WorkspacePage title="Settings" description="Manage your NEELASTACK account and workspace access." connected>
      <section className="workspace-card">
        <div className="card-heading">
          <div><p className="card-kicker">ACCOUNT</p><h2>Account management</h2></div>
        </div>
        <p className="card-description">
          Registration is available from the sign-in screen. Deleting your account permanently removes your projects, chats, agents, files, jobs, and memories.
        </p>
        {error && <div className="error-banner" role="alert">{error}</div>}
        <button className="danger-button" type="button" onClick={() => void deleteAccount()} disabled={busy}>
          {busy ? "Deleting account..." : "Delete account"}
        </button>
      </section>
    </WorkspacePage>
  );
}
