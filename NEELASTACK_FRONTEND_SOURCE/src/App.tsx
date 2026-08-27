import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import MainLayout from "./layouts/MainLayout";
import Projects from "./pages/Projects";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Register from "./pages/Register";
import ApiWorkspace from "./pages/ApiWorkspace";
import WorkspacePage from "./components/WorkspacePage";

function PlannedWorkspace({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <WorkspacePage
      title={title}
      description={description}
      connected={false}
    >
      <section className="workspace-card">
        <div className="card-heading">
          <div>
            <p className="card-kicker">MODULE</p>
            <h2>{title} workspace</h2>
          </div>

          <span className="project-status">PLANNED</span>
        </div>

        <p className="card-description">
          The active project workspace is ready. The backend API for this
          module has not been exposed yet.
        </p>
      </section>
    </WorkspacePage>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>
            <Route path="/" element={<Dashboard />} />

            <Route
              path="/chat"
              element={
                <ApiWorkspace
                  title="Chat"
                  description="Talk to NEELASTACK inside the active project workspace."
                  endpoint="/conversations"
                  label="Conversations"
                />
              }
            />

            <Route path="/projects" element={<Projects />} />

            <Route
              path="/agents"
              element={
                <ApiWorkspace
                  title="Agents"
                  description="Manage AI agents inside the active project workspace."
                  endpoint="/agents"
                  label="Registered Agents"
                />
              }
            />

            <Route
              path="/workflows"
              element={
                <ApiWorkspace
                  title="Workflows"
                  description="Build and monitor workflows inside the active project workspace."
                  endpoint="/workflows"
                  label="Available Workflows"
                />
              }
            />

            <Route
              path="/files"
              element={
                <PlannedWorkspace
                  title="Files"
                  description="Manage documents and knowledge sources for the active project."
                />
              }
            />

            <Route
              path="/mcp"
              element={
                <ApiWorkspace
                  title="MCP"
                  description="Connect and control MCP tools inside the active project workspace."
                  endpoint="/mcp/tools"
                  label="MCP Tools"
                />
              }
            />

            <Route
              path="/evaluations"
              element={
                <PlannedWorkspace
                  title="Evaluations"
                  description="Inspect quality, safety, latency and cost evaluations."
                />
              }
            />

            <Route
              path="/observability"
              element={
                <PlannedWorkspace
                  title="Observability"
                  description="Monitor system health, traces, metrics and activity."
                />
              }
            />

            <Route
              path="/security"
              element={
                <PlannedWorkspace
                  title="Security"
                  description="Review permissions, security controls and audit activity."
                />
              }
            />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
