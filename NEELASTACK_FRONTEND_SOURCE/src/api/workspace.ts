const configuredApiUrl = import.meta.env.VITE_API_URL as string | undefined;
const isDeployedHost =
  typeof window !== "undefined" &&
  window.location.hostname === "neelastack.vercel.app";
const API_BASE =
  isDeployedHost &&
  (!configuredApiUrl ||
    configuredApiUrl.includes("127.0.0.1") ||
    configuredApiUrl.includes("localhost"))
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
  return (
    localStorage.getItem("neelastack_active_project_name") ||
    "No active project"
  );
}

export async function apiGet(path: string) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      Authorization: `Bearer ${getToken()}`,
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  return response.json();
}

export async function apiPost(path: string, body: unknown) {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${getToken()}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  return response.json();
}
