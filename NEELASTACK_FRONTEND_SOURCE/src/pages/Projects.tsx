import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { createProject, getProjects, Project } from "../api/projects";

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  function activateProject(project: Project) {
    localStorage.setItem(
      "neelastack_active_project_id",
      String(project.id),
    );

    localStorage.setItem(
      "neelastack_active_project_name",
      project.name,
    );

    window.dispatchEvent(new Event("neelastack-project-changed"));

    navigate("/chat");
  }

  async function loadProjects() {
    setLoading(true);
    setError("");

    try {
      const data = await getProjects();
      setProjects(data);

      // Automatically activate the first project
      // when no project is currently selected.
      const activeId = localStorage.getItem(
        "neelastack_active_project_id",
      );

      if (!activeId && data.length > 0) {
        localStorage.setItem(
          "neelastack_active_project_id",
          String(data[0].id),
        );

        localStorage.setItem(
          "neelastack_active_project_name",
          data[0].name,
        );
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to load projects.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadProjects();
  }, []);

  async function handleCreate(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const projectName = name.trim();

    if (!projectName) {
      setError("Project name is required.");
      return;
    }

    setCreating(true);
    setError("");

    try {
      const project = await createProject({ name: projectName });

      setProjects((current) => [project, ...current]);
      setName("");

      // Newly-created project becomes active immediately.
      activateProject(project);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to create project.",
      );
    } finally {
      setCreating(false);
    }
  }

  const activeProjectId = Number(
    localStorage.getItem("neelastack_active_project_id"),
  );

  return (
    <section className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">WORKSPACE</p>
          <h1>Projects</h1>
          <p className="page-description">
            Organize agents, workflows, files and memory by project.
          </p>
        </div>

        <button
          className="secondary-button"
          type="button"
          onClick={() => void loadProjects()}
          disabled={loading}
        >
          {loading ? "Refreshing..." : "Refresh"}
        </button>
      </div>

      <div className="workspace-grid">
        <section className="workspace-card create-card">
          <div className="card-heading">
            <div>
              <p className="card-kicker">NEW PROJECT</p>
              <h2>Create project</h2>
            </div>

            <div className="card-icon">+</div>
          </div>

          <p className="card-description">
            Start a workspace for your agents, workflows and knowledge.
          </p>

          <form onSubmit={handleCreate} className="project-form">
            <label htmlFor="project-name">Project name</label>

            <input
              id="project-name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="e.g. Customer Support AI"
              disabled={creating}
            />

            <button
              className="primary-button"
              type="submit"
              disabled={creating || !name.trim()}
            >
              {creating ? "Creating..." : "Create project"}
            </button>
          </form>
        </section>

        <section className="workspace-card projects-card">
          <div className="card-heading">
            <div>
              <p className="card-kicker">PROJECTS</p>
              <h2>Your projects</h2>
            </div>

            <div className="project-count">{projects.length}</div>
          </div>

          {error && (
            <div className="error-banner" role="alert">
              {error}
            </div>
          )}

          {loading ? (
            <div className="state-card">
              <div className="loading-pulse" />
              <p>Loading projects...</p>
            </div>
          ) : projects.length === 0 ? (
            <div className="state-card empty-state">
              <div className="empty-icon">▣</div>
              <h3>No projects yet</h3>
              <p>Create your first project to get started.</p>
            </div>
          ) : (
            <div className="project-list">
              {projects.map((project) => {
                const active = project.id === activeProjectId;

                return (
                  <article
                    className="project-row"
                    key={project.id}
                    onClick={() => activateProject(project)}
                    style={{
                      cursor: "pointer",
                      border:
                        active
                          ? "1px solid rgba(100, 255, 180, 0.6)"
                          : undefined,
                    }}
                  >
                    <div className="project-mark">P</div>

                    <div className="project-info">
                      <h3>{project.name}</h3>
                      <p>Project #{project.id}</p>
                    </div>

                    <span className="project-status">
                      {active ? "ACTIVE" : "SELECT"}
                    </span>
                  </article>
                );
              })}
            </div>
          )}
        </section>
      </div>
    </section>
  );
}
