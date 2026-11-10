import { useCallback, useEffect, useState } from "react";
import { api, getToken, setToken } from "./api.js";
import Login from "./components/Login.jsx";
import Dashboard from "./components/Dashboard.jsx";
import Editor from "./components/Editor.jsx";

export default function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState("loading");
  const [openDocId, setOpenDocId] = useState(null);

  useEffect(() => {
    if (!getToken()) {
      setView("login");
      return;
    }
    api
      .me()
      .then((u) => {
        setUser(u);
        setView("dashboard");
      })
      .catch(() => {
        setToken(null);
        setView("login");
      });
  }, []);

  const handleLoggedIn = useCallback((token, u) => {
    setToken(token);
    setUser(u);
    setView("dashboard");
  }, []);

  const handleLogout = useCallback(() => {
    setToken(null);
    setUser(null);
    setOpenDocId(null);
    setView("login");
  }, []);

  const openDoc = useCallback((id) => {
    setOpenDocId(id);
    setView("editor");
  }, []);

  const backToDashboard = useCallback(() => {
    setOpenDocId(null);
    setView("dashboard");
  }, []);

  if (view === "loading") {
    return <div className="centered muted">Loading…</div>;
  }
  if (view === "login") {
    return <Login onLoggedIn={handleLoggedIn} />;
  }
  if (view === "editor") {
    return (
      <Editor
        docId={openDocId}
        currentUser={user}
        onBack={backToDashboard}
      />
    );
  }
  return (
    <Dashboard
      currentUser={user}
      onOpenDoc={openDoc}
      onLogout={handleLogout}
    />
  );
}
