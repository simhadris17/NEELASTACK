import { useEffect, useMemo, useState } from "react";
import {
  getAgents,
  getConversations,
  getProjects,
  getWorkflows,
  type Agent,
  type Conversation,
  type Project,
  type Workflow,
} from "../services/api";
import { useAuth } from "../store/auth";

interface DashboardData {
  projects: Project[];
  agents: Agent[];
  workflows: Workflow[];
  conversations: Conversation[];
}

export default function Dashboard() {
  const { user } = useAuth();

  const [data, setData] = useState<DashboardData>({
    projects: [],
    agents: [],
    workflows: [],
    conversations: [],
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function loadDashboard() {
    setLoading(true);
    setError("");

    try {
      const [projects, agents, workflows, conversations] =
        await Promise.all([
          getProjects(),
          getAgents(),
          getWorkflows(),
          getConversations(),
        ]);

      setData({
        projects,
        agents,
        workflows,
        conversations,
      });
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load dashboard data.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDashboard();
  }, []);

  const recentConversations = useMemo(() => {
    return [...data.conversations]
      .sort((a, b) => {
        const left = a.updated_at || a.created_at || "";
        const right = b.updated_at || b.created_at || "";
        return right.localeCompare(left);
      })
      .slice(0, 5);
  }, [data.conversations]);

  const stats = [
    {
      label: "Projects",
      value: data.projects.length,
      icon: "▣",
      description: "Active workspaces",
    },
    {
      label: "Agents",
      value: data.agents.length,
      icon: "◎",
      description: "Registered agents",
    },
    {
      label: "Workflows",
      value: data.workflows.length,
      icon: "⌁",
      description: "Available workflows",
    },
    {
      label: "Conversations",
      value: data.conversations.length,
      icon: "◈",
      description: "Workspace history",
    },
  ];

  return (
    <section className="page-shell dashboard-page">
      <div className="dashboard-hero">
        <div>
          <p className="eyebrow">NEELASTACK / OVERVIEW</p>

          <h1>
            Welcome back
            {user?.email ? `, ${user.email.split("@")[0]}` : ""}.
          </h1>

          <p className="page-description">
            Your AI engineering workspace, systems and activity at a glance.
          </p>
        </div>

        <button
          className="dashboard-refresh"
          type="button"
          onClick={() => void loadDashboard()}
          disabled={loading}
        >
          {loading ? "Refreshing..." : "↻ Refresh"}
        </button>
      </div>

      {error && (
        <div className="dashboard-error" role="alert">
          <strong>Unable to load workspace data</strong>
          <span>{error}</span>
        </div>
      )}

      <div className="stats-grid">
        {stats.map((stat) => (
          <article className="stat-card" key={stat.label}>
            <div className="stat-card-top">
              <span className="stat-icon">{stat.icon}</span>
              <span className="stat-label">{stat.label}</span>
            </div>

            <div className="stat-value">
              {loading ? "—" : stat.value}
            </div>

            <div className="stat-description">
              {stat.description}
            </div>
          </article>
        ))}
      </div>

      <div className="dashboard-grid">
        <section className="dashboard-panel">
          <div className="panel-heading">
            <div>
              <p className="panel-eyebrow">WORKSPACE</p>
              <h2>Projects</h2>
            </div>

            <span className="panel-count">
              {loading ? "..." : data.projects.length}
            </span>
          </div>

          {loading ? (
            <div className="panel-empty">Loading projects...</div>
          ) : data.projects.length === 0 ? (
            <div className="panel-empty">
              <span className="empty-icon">▣</span>
              <strong>No projects yet</strong>
              <p>Create your first project to organize your AI work.</p>
            </div>
          ) : (
            <div className="resource-list">
              {data.projects.slice(0, 5).map((project) => (
                <div className="resource-row" key={project.id}>
                  <div className="resource-icon">▣</div>
                  <div className="resource-content">
                    <strong>{project.name}</strong>
                    <span>
                      {project.description || "NEELASTACK project"}
                    </span>
                  </div>
                  <span className="resource-arrow">→</span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="dashboard-panel">
          <div className="panel-heading">
            <div>
              <p className="panel-eyebrow">INTELLIGENCE</p>
              <h2>Agents</h2>
            </div>

            <span className="panel-count">
              {loading ? "..." : data.agents.length}
            </span>
          </div>

          {loading ? (
            <div className="panel-empty">Loading agents...</div>
          ) : data.agents.length === 0 ? (
            <div className="panel-empty">
              <span className="empty-icon">◎</span>
              <strong>No agents yet</strong>
              <p>Your registered AI agents will appear here.</p>
            </div>
          ) : (
            <div className="resource-list">
              {data.agents.slice(0, 5).map((agent) => (
                <div className="resource-row" key={agent.id}>
                  <div className="resource-icon agent-icon">◎</div>
                  <div className="resource-content">
                    <strong>{agent.name}</strong>
                    <span>
                      {agent.role || agent.description || "AI agent"}
                    </span>
                  </div>
                  <span className="resource-status">READY</span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="dashboard-panel">
          <div className="panel-heading">
            <div>
              <p className="panel-eyebrow">AUTOMATION</p>
              <h2>Workflows</h2>
            </div>

            <span className="panel-count">
              {loading ? "..." : data.workflows.length}
            </span>
          </div>

          {loading ? (
            <div className="panel-empty">Loading workflows...</div>
          ) : data.workflows.length === 0 ? (
            <div className="panel-empty">
              <span className="empty-icon">⌁</span>
              <strong>No workflows yet</strong>
              <p>Build multi-step automation from the Workflows workspace.</p>
            </div>
          ) : (
            <div className="resource-list">
              {data.workflows.slice(0, 5).map((workflow) => (
                <div className="resource-row" key={workflow.id}>
                  <div className="resource-icon workflow-icon">⌁</div>
                  <div className="resource-content">
                    <strong>{workflow.name}</strong>
                    <span>Multi-step AI workflow</span>
                  </div>
                  <span className="resource-status">READY</span>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="dashboard-panel">
          <div className="panel-heading">
            <div>
              <p className="panel-eyebrow">ACTIVITY</p>
              <h2>Recent conversations</h2>
            </div>

            <span className="panel-count">
              {loading ? "..." : recentConversations.length}
            </span>
          </div>

          {loading ? (
            <div className="panel-empty">Loading activity...</div>
          ) : recentConversations.length === 0 ? (
            <div className="panel-empty">
              <span className="empty-icon">◈</span>
              <strong>No conversations yet</strong>
              <p>Start a conversation with NEELASTACK to see activity here.</p>
            </div>
          ) : (
            <div className="resource-list">
              {recentConversations.map((conversation) => (
                <div
                  className="resource-row"
                  key={conversation.id}
                >
                  <div className="resource-icon">◈</div>

                  <div className="resource-content">
                    <strong>
                      {conversation.title || `Conversation #${conversation.id}`}
                    </strong>
                    <span>
                      {conversation.updated_at ||
                        conversation.created_at ||
                        "Recent activity"}
                    </span>
                  </div>

                  <span className="resource-arrow">→</span>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>

      <section className="system-panel">
        <div className="system-panel-left">
          <div className="system-online-dot" />

          <div>
            <strong>NEELASTACK SYSTEM ONLINE</strong>
            <span>Authenticated backend connection established</span>
          </div>
        </div>

        <div className="system-metrics">
          <div>
            <span>API</span>
            <strong>CONNECTED</strong>
          </div>

          <div>
            <span>AUTH</span>
            <strong>SECURE</strong>
          </div>

          <div>
            <span>MODE</span>
            <strong>PRODUCTION</strong>
          </div>
        </div>
      </section>
    </section>
  );
}
