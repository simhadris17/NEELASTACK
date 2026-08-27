const deployedApiUrl = "https://neelastack.onrender.com";
const localApiUrl = "http://127.0.0.1:8000";

export const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  (typeof window !== "undefined" && window.location.hostname === "neelastack.vercel.app"
    ? deployedApiUrl
    : localApiUrl);

export const TOKEN_KEY = "neelastack_token";

export interface AuthUser {
  id?: number | string;
  email: string;
  role?: string;
  [key: string]: unknown;
}

interface AuthResponse {
  access_token: string;
  token_type?: string;
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

export async function register(
  email: string,
  password: string,
): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Registration failed");
  }

  const result = data as AuthResponse;

  if (!result.access_token) {
    throw new Error("Registration succeeded but no access token was returned");
  }

  setToken(result.access_token);

  return await getCurrentUser(result.access_token);
}

export async function login(
  email: string,
  password: string,
): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email,
      password,
    }),
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  const result = data as AuthResponse;

  if (!result.access_token) {
    throw new Error("Login succeeded but no access token was returned");
  }

  setToken(result.access_token);

  try {
    return await getCurrentUser(result.access_token);
  } catch (error) {
    clearToken();
    throw error;
  }
}

export async function getCurrentUser(
  suppliedToken?: string,
): Promise<AuthUser> {
  const token = suppliedToken || getToken();

  if (!token) {
    throw new Error("Authentication required");
  }

  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    clearToken();
    throw new Error(data.detail || "Session expired");
  }

  return data as AuthUser;
}

export function logout(): void {
  clearToken();
}
