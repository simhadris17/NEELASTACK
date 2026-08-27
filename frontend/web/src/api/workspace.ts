const configuredApiUrl = import.meta.env.VITE_API_URL as string | undefined;
const isDeployedHost =
  typeof window !== "undefined" &&
  window.location.hostname === "neelastack.vercel.app";
const API_BASE =
  isDeployedHost &&
  (!configuredApiUrl || configuredApiUrl.includes("127.0.0.1") || configuredApiUrl.includes("localhost"))
    ? "https://neelastack.onrender.com"
    : configuredApiUrl || "http://127.0.0.1:8000";

export function getToken(): string {
  return localStorage.getItem("neelastack_token") || "";
}

export function getActiveProjectId(): number | null {
  const value = localStorage.getItem("neelastack_active_project_id");
  if (!value) return null;
  const id = Number(value);
  return Number.isFinite(id) ? id : null;
}

export function getActiveProjectName(): string {
  return localStorage.getItem("neelastack_active_project_name") || "No active project";
}

function authHeaders(extra: Record<string, string> = {}) {
  return { Authorization: `Bearer ${getToken()}`, ...extra };
}

async function responseData(response: Response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || `Request failed: ${response.status}`);
  return data;
}

export async function apiGet(path: string) {
  return responseData(await fetch(`${API_BASE}${path}`, { headers: authHeaders() }));
}

export async function apiPost(path: string, body: unknown) {
  return responseData(await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: authHeaders({ "Content-Type": "application/json" }),
    body: JSON.stringify(body),
  }));
}

export async function apiDelete(path: string) {
  return responseData(await fetch(`${API_BASE}${path}`, { method: "DELETE", headers: authHeaders() }));
}

export async function apiUpload(path: string, file: File) {
  const form = new FormData();
  form.append("file", file);
  return responseData(await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: authHeaders(),
    body: form,
  }));
}
