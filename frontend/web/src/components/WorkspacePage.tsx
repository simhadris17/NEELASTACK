import { ReactNode } from "react";

type WorkspaceProps = {
  title: string;
  description: string;
  children: ReactNode;
  connected?: boolean;
};

export default function WorkspacePage({
  title,
  description,
  children,
  connected = true,
}: WorkspaceProps) {
  const projectName =
    localStorage.getItem("neelastack_active_project_name") ||
    "No active project";

  const projectId =
    localStorage.getItem("neelastack_active_project_id");

  return (
    <section className="page-shell">
      <div className="page-header">
        <div>
          <p className="eyebrow">NEELASTACK / PROJECT WORKSPACE</p>
          <h1>{title}</h1>
          <p className="page-description">{description}</p>
        </div>
      </div>

      <section className="workspace-card active-project-card">
        <div className="card-heading">
          <div>
            <p className="card-kicker">ACTIVE WORKSPACE</p>
            <h2>{projectName}</h2>
          </div>

          <span className="project-status">
            {connected ? "ACTIVE" : "PLANNED"}
          </span>
        </div>

        <p className="card-description">
          {connected
            ? "This workspace is active and connected to the NEELASTACK project."
            : "This workspace is ready for the corresponding backend module."}
        </p>

        {projectId && (
          <div className="active-project-meta">
            <span>Project #{projectId}</span>
            <span>{connected ? "Backend connected" : "Backend pending"}</span>
          </div>
        )}
      </section>

      {children}
    </section>
  );
}
