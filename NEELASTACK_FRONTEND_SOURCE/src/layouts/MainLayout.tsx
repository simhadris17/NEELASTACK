import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../store/auth";

const navItems = [
  { to: "/", label: "Dashboard", icon: "⌂", end: true },
  { to: "/chat", label: "Chat", icon: "◈" },
  { to: "/projects", label: "Projects", icon: "▣" },
  { to: "/agents", label: "Agents", icon: "◎" },
  { to: "/workflows", label: "Workflows", icon: "⌁" },
  { to: "/files", label: "Files", icon: "□" },
  { to: "/mcp", label: "MCP", icon: "◇" },
  { to: "/evaluations", label: "Evaluations", icon: "✓" },
  { to: "/observability", label: "Observability", icon: "◌" },
  { to: "/security", label: "Security", icon: "◇" },
];

export default function MainLayout() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">N</div>

          <div>
            <div className="brand-name">NEELASTACK</div>
            <div className="brand-subtitle">AI ENGINEERING</div>
          </div>
        </div>

        <div className="workspace-label">WORKSPACE</div>

        <nav className="nav-list">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) =>
                `nav-item ${isActive ? "active" : ""}`
              }
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="status-dot" />

          <div>
            <div className="system-status">SYSTEM ONLINE</div>
            <div className="system-version">NEELASTACK v0.1</div>
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">Workspace / Overview</div>

          <div className="topbar-actions">
            <button
              className="topbar-button"
              type="button"
              title="Command palette"
            >
              ⌘ K
            </button>

            <div className="user-menu">
              <button className="avatar" type="button">
                {(user?.email?.[0] || "S").toUpperCase()}
              </button>

              <div className="user-menu-info">
                <strong>{user?.email || "User"}</strong>
                <span>{user?.role || "user"}</span>
              </div>

              <button
                className="logout-button"
                type="button"
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <div className="content-area">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
