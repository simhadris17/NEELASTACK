import { useCallback, useEffect, useState } from "react";
import {
  getCurrentUser,
  getToken,
  login as loginRequest,
  logout as logoutRequest,
  type AuthUser,
} from "../services/auth";

export interface AuthState {
  user: AuthUser | null;
  loading: boolean;
  error: string;
}

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const restoreSession = useCallback(async () => {
    const token = getToken();

    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const currentUser = await getCurrentUser(token);
      setUser(currentUser);
      setError("");
    } catch {
      setUser(null);
      setError("");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void restoreSession();
  }, [restoreSession]);

  async function login(email: string, password: string) {
    setLoading(true);
    setError("");

    try {
      const currentUser = await loginRequest(email, password);
      setUser(currentUser);
      return currentUser;
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Login failed";

      setUser(null);
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    logoutRequest();
    setUser(null);
    setError("");
  }

  return {
    user,
    loading,
    error,
    isAuthenticated: Boolean(user),
    login,
    logout,
    restoreSession,
  };
}
