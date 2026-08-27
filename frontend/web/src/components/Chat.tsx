import { FormEvent, KeyboardEvent, useEffect, useRef, useState } from "react";
import {
  apiGet,
  apiPost,
  getActiveProjectName,
} from "../api/workspace";

type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

type Conversation = {
  id?: number;
  title?: string;
  created_at?: string;
  updated_at?: string;
};

export default function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [error, setError] = useState("");

  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const projectName = getActiveProjectName();

  useEffect(() => {
    void loadConversations();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, loading]);

  async function loadConversations() {
    setLoadingHistory(true);
    setError("");

    try {
      const result = await apiGet("/conversations");

      const items = Array.isArray(result)
        ? result
        : Array.isArray(result?.conversations)
          ? result.conversations
          : [];

      setConversations(items);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load conversations.",
      );
    } finally {
      setLoadingHistory(false);
    }
  }

  async function loadConversation(id: number) {
    setLoadingHistory(true);
    setError("");

    try {
      const result = await apiGet(`/conversations/${id}`);

      const rawMessages = Array.isArray(result)
        ? result
        : Array.isArray(result?.messages)
          ? result.messages
          : [];

      const normalized: Message[] = rawMessages
        .map((item: any, index: number) => ({
          id: String(item.id ?? `${id}-${index}`),
          role:
            item.role === "user" || item.role === "assistant"
              ? item.role
              : item.sender === "user"
                ? "user"
                : "assistant",
          content: String(
            item.content ??
              item.message ??
              item.text ??
              "",
          ),
        }))
        .filter((item: Message) => item.content);

      setConversationId(id);
      setMessages(normalized);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load conversation.",
      );
    } finally {
      setLoadingHistory(false);
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  }

  function startNewChat() {
    setConversationId(null);
    setMessages([]);
    setInput("");
    setError("");

    requestAnimationFrame(() => inputRef.current?.focus());
  }

  async function sendMessage(event?: FormEvent) {
    event?.preventDefault();

    const message = input.trim();

    if (!message || loading) {
      return;
    }

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: "user",
      content: message,
    };

    setMessages((current) => [...current, userMessage]);
    setInput("");
    setError("");
    setLoading(true);

    try {
      const result = await apiPost("/chat", {
        message,
        conversation_id: conversationId,
      });

      const nextConversationId =
        result?.conversation_id ??
        result?.conversation?.id ??
        conversationId;

      if (typeof nextConversationId === "number") {
        setConversationId(nextConversationId);
      }

      const answer =
        result?.response ??
        result?.message ??
        result?.content ??
        result?.answer ??
        result?.reply ??
        result?.text;

      const assistantContent =
        typeof answer === "string"
          ? answer
          : result?.plan
            ? String(result.plan)
            : JSON.stringify(result, null, 2);

      setMessages((current) => [
        ...current,
        {
          id: `assistant-${Date.now()}`,
          role: "assistant",
          content: assistantContent,
        },
      ]);

      void loadConversations();
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Unable to send message.";

      setError(message);

      setMessages((current) => [
        ...current,
        {
          id: `assistant-error-${Date.now()}`,
          role: "assistant",
          content:
            "I couldn't complete that request. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);

      requestAnimationFrame(() => {
        inputRef.current?.focus();
      });
    }
  }

  function handleInputKeyDown(
    event: KeyboardEvent<HTMLTextAreaElement>,
  ) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      if (!loading) {
        void sendMessage();
      }
    }
  }

  return (
    <section className="chat-page">
      <aside className="chat-sidebar">
        <button
          className="chat-new-button"
          type="button"
          onClick={startNewChat}
        >
          <span>＋</span>
          <span>New chat</span>
        </button>

        <div className="chat-search">
          <span>⌕</span>
          <input
            type="text"
            placeholder="Search"
            aria-label="Search conversations"
          />
        </div>

        <div className="chat-section-label">CHATS</div>

        <div className="conversation-list">
          {loadingHistory && conversations.length === 0 ? (
            <div className="conversation-muted">
              Loading chats...
            </div>
          ) : conversations.length === 0 ? (
            <div className="conversation-muted">
              No previous conversations
            </div>
          ) : (
            conversations.map((conversation, index) => {
              const id = Number(conversation.id);

              return (
                <button
                  key={conversation.id ?? index}
                  className={
                    conversationId === id
                      ? "conversation-item active"
                      : "conversation-item"
                  }
                  type="button"
                  onClick={() => {
                    if (Number.isFinite(id)) {
                      void loadConversation(id);
                    }
                  }}
                >
                  <span className="conversation-icon">◈</span>
                  <span className="conversation-title">
                    {conversation.title ||
                      `Conversation ${id || index + 1}`}
                  </span>
                </button>
              );
            })
          )}
        </div>

        <div className="chat-sidebar-bottom">
          <span className="chat-online-dot" />
          <span>NEELASTACK ONLINE</span>
        </div>
      </aside>

      <main className="chat-main">
        <header className="chat-header">
          <div>
            <div className="chat-header-title">Chat</div>
            <div className="chat-header-subtitle">
              NEELASTACK / PROJECT WORKSPACE
            </div>
          </div>

          <div className="chat-project-status">
            <span className="chat-status-dot" />
            <span>{projectName}</span>
            <strong>ACTIVE</strong>
          </div>
        </header>

        <div className="chat-content">
          {messages.length === 0 ? (
            <div className="chat-welcome">
              <div className="chat-logo">N</div>

              <h1>NEELASTACK</h1>

              <p>
                How can I help you?
              </p>

              <span>
                Ask anything about your active project.
              </span>
            </div>
          ) : (
            <div className="message-list">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`chat-message-row ${message.role}`}
                >
                  <div className="chat-message-avatar">
                    {message.role === "user" ? "S" : "N"}
                  </div>

                  <div className="chat-message-body">
                    <div className="chat-message-role">
                      {message.role === "user"
                        ? "You"
                        : "NEELASTACK"}
                    </div>

                    <div className="chat-message-content">
                      {message.content}
                    </div>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="chat-message-row assistant">
                  <div className="chat-message-avatar">N</div>

                  <div className="chat-message-body">
                    <div className="chat-message-role">
                      NEELASTACK
                    </div>

                    <div className="chat-thinking">
                      <span />
                      <span />
                      <span />
                      <em>Thinking...</em>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>
          )}

          {error && (
            <div className="chat-error" role="alert">
              {error}
            </div>
          )}
        </div>

        <div className="chat-composer-area">
          <form
            className="chat-composer"
            onSubmit={sendMessage}
          >
            <textarea
              ref={inputRef}
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleInputKeyDown}
              placeholder="Type your message..."
              rows={1}
              disabled={loading}
              aria-label="Message"
            />

            <div className="chat-composer-actions">
              <button
                className="chat-attach-button"
                type="button"
                title="Attach"
                disabled={loading}
              >
                ＋
              </button>

              <button
                className="chat-send-button"
                type="submit"
                disabled={!input.trim() || loading}
                title="Send"
              >
                ➤
              </button>
            </div>
          </form>

          <div className="chat-disclaimer">
            NEELASTACK can make mistakes. Check important information.
          </div>
        </div>
      </main>
    </section>
  );
}
