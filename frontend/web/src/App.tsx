import { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [email, setEmail] = useState("test@example.com");
  const [password, setPassword] = useState("Test@123456");
  const [token, setToken] = useState("");
  const [user, setUser] = useState("");
  const [q, setQ] = useState("");
  const [a, setA] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  async function login() {
    setStatus("Logging in...");
    try {
      const r = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await r.json();

      if (!r.ok) {
        setStatus(data.detail || "Login failed");
        return;
      }

      setToken(data.access_token);
      localStorage.setItem("neelastack_token", data.access_token);

      const me = await fetch(`${API}/auth/me`, {
        headers: {
          Authorization: `Bearer ${data.access_token}`,
        },
      });

      const meData = await me.json();

      if (me.ok) {
        setUser(meData.email);
        setStatus("Login successful");
      } else {
        setStatus("Login successful, but /auth/me failed");
      }
    } catch {
      setStatus("Backend connection failed");
    }
  }

  async function send() {
    if (!q.trim()) return;

    let activeToken = token || localStorage.getItem("neelastack_token");

    if (!activeToken) {
      setStatus("Please login first");
      return;
    }

    setLoading(true);
    setA("");

    try {
      const r = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${activeToken}`,
        },
        body: JSON.stringify({
          message: q,
        }),
      });

      const data = await r.json();

      if (!r.ok) {
        setA(data.detail || "Chat request failed");
        return;
      }

      setA(data.answer || "No response");
      setStatus(`Chat successful — conversation ${data.conversation_id}`);
    } catch {
      setA("Backend connection failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main
      style={{
        minHeight: "100vh",
        background: "#09090b",
        color: "white",
        padding: 40,
        fontFamily: "Inter, system-ui",
      }}
    >
      <h1>NEELASTACK</h1>
      <p>AI Engineering Workspace</p>

      <section style={{ maxWidth: 600 }}>
        <h2>Login</h2>

        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          style={{ width: "100%", padding: 10, marginBottom: 10 }}
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          style={{ width: "100%", padding: 10, marginBottom: 10 }}
        />

        <button onClick={login}>
          Login
        </button>

        <p>{status}</p>

        {user && (
          <p>
            Logged in as: <strong>{user}</strong>
          </p>
        )}

        <hr />

        <h2>Chat</h2>

        <textarea
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask NEELASTACK..."
          style={{
            width: "100%",
            minHeight: 120,
            padding: 10,
            marginBottom: 10,
          }}
        />

        <br />

        <button onClick={send} disabled={loading || !token}>
          {loading ? "Thinking..." : "Send"}
        </button>

        <pre
          style={{
            whiteSpace: "pre-wrap",
            marginTop: 20,
          }}
        >
          {a}
        </pre>
      </section>
    </main>
  );
}
