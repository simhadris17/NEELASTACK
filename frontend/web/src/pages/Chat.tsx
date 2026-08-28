import { FormEvent, useState } from "react";
import { ReactNode } from "react";
import VoiceControls from "../components/VoiceControls";

type Message = {
  role: "user" | "assistant";
  content: string;
};

type ChatResponse = {
  conversation_id: number;
  answer: string;
};

function renderMarkdown(content: string): ReactNode[] {
  const parts = content.split(/```([^\n]*)\n([\s\S]*?)```/g);
  const nodes: ReactNode[] = [];
  for (let index = 0; index < parts.length; index += 3) {
    const text = parts[index];
    if (text) {
      text.split("\n").forEach((line, lineIndex) => {
        const key = `${index}-${lineIndex}`;
        if (/^\s*[A-Za-z+#.-]+Copy\s*$/.test(line)) return;
        if (!line.trim()) {
          nodes.push(<div className="chat-markdown-spacer" key={key} />);
        } else if (line.startsWith("### ")) {
          nodes.push(<h4 key={key}>{line.slice(4)}</h4>);
        } else if (line.startsWith("## ")) {
          nodes.push(<h3 key={key}>{line.slice(3)}</h3>);
        } else if (line.startsWith("# ")) {
          nodes.push(<h2 key={key}>{line.slice(2)}</h2>);
        } else if (/^\s*[-*]\s+/.test(line) || /^\s*\d+\.\s+/.test(line)) {
          nodes.push(
            <li key={key}>{line.replace(/^\s*(?:[-*]|\d+\.)\s+/, "")}</li>,
          );
        } else {
          nodes.push(<p key={key}>{line}</p>);
        }
      });
    }

    const language = parts[index + 1]?.replace(/Copy$/, "");
    const code = parts[index + 2];
    if (code !== undefined) {
      nodes.push(
        <div className="chat-code-block" key={`code-${index}`}>
          <div className="chat-code-header">
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
  return nodes;
}

const API_BASE =
  window.location.hostname === "neelastack.vercel.app"
    ? "https://neelastack.onrender.com"
    : "http://127.0.0.1:8000";

const CHAT_API = `${API_BASE}/api/v1/chat`;

function getToken(): string {
  return localStorage.getItem("neelastack_token") || "";
}

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function sendMessage(event: FormEvent) {
    event.preventDefault();

    const message = input.trim();

    if (!message || loading) {
      return;
    }

    setError("");

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: message,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const token = getToken();

      if (!token) {
        throw new Error("Authentication token not found. Please login again.");
      }

      const response = await fetch(CHAT_API, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || `Chat request failed: ${response.status}`);
      }

      const data = (await response.json()) as ChatResponse;

      setConversationId(data.conversation_id);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to get a response from NEELASTACK.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">NEELASTACK / PROJECT WORKSPACE</p>
          <h1>Chat</h1>
          <p className="page-description">
            Talk to NEELASTACK inside the active project workspace.
          </p>
        </div>
      </div>

      <section
        className="workspace-card"
        style={{
          minHeight: "620px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div className="card-heading">
          <div>
            <p className="card-kicker">NEELASTACK</p>
            <h2>How can I help you?</h2>
          </div>

          {conversationId && (
            <span className="project-status">
              CONVERSATION #{conversationId}
            </span>
          )}
        </div>

        <div
          style={{
            flex: 1,
            overflowY: "auto",
            marginTop: "24px",
            padding: "8px 2px",
          }}
        >
          {messages.length === 0 ? (
            <div className="state-card">
              <div className="empty-icon">N</div>
              <h3>Start a conversation</h3>
              <p>
                Type a message below and NEELASTACK will respond.
              </p>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={`${message.role}-${index}`}
                style={{
                  display: "flex",
                  justifyContent:
                    message.role === "user" ? "flex-end" : "flex-start",
                  marginBottom: "14px",
                }}
              >
                <div
                  style={{
                    maxWidth: "78%",
                    padding: "12px 15px",
                    borderRadius: "12px",
                    border:
                      message.role === "user"
                        ? "1px solid rgba(96, 165, 250, 0.22)"
                        : "1px solid rgba(255, 255, 255, 0.07)",
                    background:
                      message.role === "user"
                        ? "rgba(59, 130, 246, 0.10)"
                        : "rgba(255, 255, 255, 0.025)",
                    color:
                      message.role === "user" ? "#dbeafe" : "#cbd5e1",
                    whiteSpace: "pre-wrap",
                    lineHeight: 1.6,
                    fontSize: "13px",
                  }}
                >
                  <div
                    style={{
                      marginBottom: "5px",
                      fontSize: "9px",
                      fontWeight: 800,
                      letterSpacing: "0.12em",
                      color:
                        message.role === "user"
                          ? "#60a5fa"
                          : "#4ade80",
                    }}
                  >
                    {message.role === "user" ? "YOU" : "NEELASTACK"}
                  </div>

                  {message.role === "assistant" ? (
                    <div className="chat-markdown">
                      {renderMarkdown(message.content)}
                    </div>
                  ) : (
                    message.content
                  )}
                </div>
              </div>
            ))
          )}

          {loading && (
            <div
              style={{
                display: "flex",
                justifyContent: "flex-start",
                marginBottom: "14px",
              }}
            >
              <div
                style={{
                  padding: "12px 15px",
                  borderRadius: "12px",
                  border: "1px solid rgba(255, 255, 255, 0.07)",
                  background: "rgba(255, 255, 255, 0.025)",
                  color: "#64748b",
                  fontSize: "12px",
                }}
              >
                NEELASTACK is thinking...
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="error-banner" role="alert">
            {error}
          </div>
        )}

        <form
          onSubmit={sendMessage}
          style={{
            display: "flex",
            gap: "10px",
            alignItems: "flex-end",
            marginTop: "18px",
            padding: "12px",
            border: "1px solid rgba(255, 255, 255, 0.08)",
            borderRadius: "12px",
            background: "rgba(0, 0, 0, 0.18)",
          }}
        >
          <textarea
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter" && !event.shiftKey) {
                event.preventDefault();
                event.currentTarget.form?.requestSubmit();
              }
            }}
            placeholder="Type your message..."
            disabled={loading}
            rows={2}
            style={{
              flex: 1,
              resize: "none",
              border: "none",
              outline: "none",
              background: "transparent",
              color: "#f8fafc",
              fontSize: "13px",
              lineHeight: 1.5,
            }}
          />

          <button
            type="submit"
            className="primary-button"
            disabled={loading || !input.trim()}
            style={{
              minWidth: "48px",
              marginTop: 0,
            }}
          >
            {loading ? "..." : "?"}
          </button>
        </form>
        <VoiceControls
          onTranscript={(transcript) => setInput((current) => `${current}${current ? " " : ""}${transcript}`)}
          speakText={messages.filter((message) => message.role === "assistant").at(-1)?.content}
        />

        <p
          style={{
            margin: "10px 0 0",
            textAlign: "center",
            color: "#475569",
            fontSize: "9px",
          }}
        >
          NEELASTACK can make mistakes
        </p>
      </section>
    </section>
  );
}
