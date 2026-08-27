export type Project = {
  id: number;
  name: string;
  created_at?: string;
};

export type CreateProjectInput = {
  name: string;
};

const API = "http://127.0.0.1:8000";

function authHeaders(): HeadersInit {
  const token = localStorage.getItem("neelastack_token");

  return {
    "Content-Type": "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function parseResponse(response: Response) {
  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const detail =
      data?.detail ||
      data?.message ||
      `Request failed with status ${response.status}`;

    throw new Error(detail);
  }

  return data;
}

export async function getProjects(): Promise<Project[]> {
  const response = await fetch(`${API}/projects`, {
    method: "GET",
    headers: authHeaders(),
  });

  const data = await parseResponse(response);

  if (Array.isArray(data)) {
    return data;
  }

  if (Array.isArray(data?.projects)) {
    return data.projects;
  }

  return [];
}

export async function createProject(
  input: CreateProjectInput,
): Promise<Project> {
  const response = await fetch(`${API}/projects`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify(input),
  });

  return parseResponse(response);
}
