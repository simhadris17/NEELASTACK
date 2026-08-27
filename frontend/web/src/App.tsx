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
import Chat from "./pages/Chat";
import ApiWorkspace from "./pages/ApiWorkspace";
import Agents from "./pages/Agents";
import WorkspacePage from "./components/WorkspacePage";
import Files from "./pages/Files";
import Workflows from "./pages/Workflows";
import MCP from "./pages/MCP";
import Evaluations from "./pages/Evaluations";
import Observability from "./pages/Observability";
import Security from "./pages/Security";
import Settings from "./pages/Settings";

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

            <Route path="/chat" element={<Chat />} />

            <Route path="/projects" element={<Projects />} />

            <Route
              path="/agents"
              element={
                <Agents />
              }
            />

            <Route
              path="/workflows"
              element={<Workflows />}
            />

            <Route
              path="/files"
              element={<Files />}
            />

            <Route
              path="/mcp"
              element={<MCP />}
            />

            <Route
              path="/evaluations"
              element={<Evaluations />}
            />

            <Route
              path="/observability"
              element={<Observability />}
            />

            <Route
              path="/security"
              element={<Security />}
            />
            <Route path="/settings" element={<Settings />} />

            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
