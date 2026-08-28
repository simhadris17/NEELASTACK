import { getToken } from "./auth";
import { API_BASE_URL } from "../api/base";

export async function apiGet<T>(path: string): Promise<T> {
  const token = getToken();

  if (!token) {
    throw new Error("Authentication required");
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || `Request failed: ${response.status}`);
  }

  return data as T;
}

export interface Project {
  id: number | string;
  name: string;
  description?: string | null;
  created_at?: string;
}

export interface Agent {
  id: number | string;
  name: string;
  description?: string | null;
  role?: string;
  created_at?: string;
}

export interface Workflow {
  id: number | string;
  name: string;
  definition_json?: string;
  created_at?: string;
}

export interface Conversation {
  id: number | string;
  title?: string | null;
  created_at?: string;
  updated_at?: string;
}

export function getProjects() {
  return apiGet<{ projects: Project[] }>("/projects").then((data) => data.projects);
}
export function getAgents() {
  return apiGet<{ agents: Agent[] }>("/agents").then((data) => data.agents);
}
export function getWorkflows() {
  return apiGet<{ workflows: Workflow[] }>("/workflows").then((data) => data.workflows);
}

export function getConversations() {
  return apiGet<{ conversations: Conversation[] }>("/conversations")
    .then((data) => data.conversations);
}
