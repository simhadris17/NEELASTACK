import { useState } from "react";
import { api } from "../services/api";

export function useChat(token: string | null) {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  async function send(message: string) {
    if (!token || !message.trim()) return;
    setLoading(true); setError("");
    try { setAnswer((await api<{ answer: string }>("/api/v1/chat", { method: "POST", token, body: { message } })).answer); }
    catch (e) { setError(e instanceof Error ? e.message : "Chat request failed"); }
    finally { setLoading(false); }
  }
  return { answer, loading, error, send };
}
