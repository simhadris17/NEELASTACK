const runtime = globalThis as typeof globalThis & { process?: { env?: Record<string, string> } };
export const API_BASE_URL = runtime.process?.env?.EXPO_PUBLIC_API_URL || "http://127.0.0.1:8000";
let accessToken: string | null = null;

async function request<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  const bearer = token || accessToken;
  if (bearer) headers.set("Authorization", `Bearer ${bearer}`);
  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || `Request failed (${response.status})`);
  return data as T;
}

export function api<T>(path: string, options: { method?: string; token?: string; body?: unknown } = {}) {
  return request<T>(path, { method: options.method || "GET", body: options.body === undefined ? undefined : JSON.stringify(options.body) }, options.token);
}

type AuthResponse = { access_token: string };
async function authenticate(path: string, email: string, password: string) {
  const result = await request<AuthResponse>(path, { method: "POST", body: JSON.stringify({ email, password }) });
  accessToken = result.access_token;
  return accessToken;
}
export const login = (email: string, password: string) => authenticate("/auth/login", email, password);
export const register = (email: string, password: string) => authenticate("/auth/register", email, password);
export function logout() { accessToken = null; }
