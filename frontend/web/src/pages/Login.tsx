import { FormEvent, useEffect, useState } from "react";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../store/auth";

export default function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  const { user, loading, error, login } = useAuth();

  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("Test@123456");
  const [submitting, setSubmitting] = useState(false);
  const [localError, setLocalError] = useState("");

  const from =
    (location.state as { from?: string } | null)?.from || "/";

  useEffect(() => {
    if (user) {
      navigate(from, { replace: true });
    }
  }, [user, navigate, from]);

  if (loading && !submitting) {
    return (
      <div className="auth-page">
        <div className="auth-card">
          <div className="auth-brand-mark">N</div>
          <p className="auth-eyebrow">NEELASTACK</p>
          <h1>Checking session</h1>
          <p className="auth-description">
            Restoring your secure workspace session...
          </p>
        </div>
      </div>
    );
  }

  if (user) {
    return <Navigate to={from} replace />;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!email.trim() || !password) {
      setLocalError("Email and password are required.");
      return;
    }

    setLocalError("");
    setSubmitting(true);

    try {
      await login(email.trim(), password);
      navigate(from, { replace: true });
    } catch {
      // Auth store exposes the backend error.
    } finally {
      setSubmitting(false);
    }
  }

  const visibleError = localError || error;

  return (
    <main className="auth-page">
      <div className="auth-background-glow" />

      <section className="auth-card">
        <div className="auth-brand">
          <div className="auth-brand-mark">N</div>

          <div>
            <div className="auth-brand-name">NEELASTACK</div>
            <div className="auth-brand-subtitle">
              AI ENGINEERING WORKSPACE
            </div>
          </div>
        </div>

        <div className="auth-heading">
          <p className="auth-eyebrow">SECURE ACCESS</p>
          <h1>Welcome back.</h1>
          <p className="auth-description">
            Sign in to continue to your AI engineering workspace.
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            <span>Email</span>
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
              autoComplete="email"
              disabled={submitting}
            />
          </label>

          <label>
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter your password"
              autoComplete="current-password"
              disabled={submitting}
            />
          </label>

          {visibleError && (
            <div className="auth-error" role="alert">
              {visibleError}
            </div>
          )}

          <button
            className="auth-submit"
            type="submit"
            disabled={submitting}
          >
            {submitting ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <div className="auth-footer">
          <span className="auth-status-dot" />
          <span>Secure backend connection</span>
        </div>
        <div className="auth-switch">
          New to NEELASTACK?{" "}
          <button type="button" onClick={() => navigate("/register")} disabled={submitting}>
            Create account
          </button>
        </div>
      </section>
    </main>
  );
}
