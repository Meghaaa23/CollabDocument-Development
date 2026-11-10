// Thin API client. All calls go to same-origin "/api/..." (Vite proxies to the
// backend in dev; FastAPI serves both in prod). The JWT is kept in localStorage
// and attached as a Bearer token.

const TOKEN_KEY = "collabdocs_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}
export function setToken(t) {
  if (t) localStorage.setItem(TOKEN_KEY, t);
  else localStorage.removeItem(TOKEN_KEY);
}

class ApiError extends Error {
  constructor(status, detail) {
    super(detail || `Request failed (${status})`);
    this.status = status;
    this.detail = detail;
  }
}

async function request(path, { method = "GET", body, isForm = false } = {}) {
  const headers = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let payload;
  if (isForm) {
    payload = body; // FormData; browser sets the content-type/boundary
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  const res = await fetch(`/api${path}`, { method, headers, body: payload });

  if (res.status === 204) return null;

  let data = null;
  const text = await res.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = text;
    }
  }

  if (!res.ok) {
    const detail =
      data && typeof data === "object" && data.detail
        ? typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail)
        : `Request failed (${res.status})`;
    throw new ApiError(res.status, detail);
  }
  return data;
}

export const api = {
  login: (email, password) =>
    request("/auth/login", { method: "POST", body: { email, password } }),
  me: () => request("/auth/me"),

  listDocuments: () => request("/documents"),
  getDocument: (id) => request(`/documents/${id}`),
  createDocument: (title, content = "") =>
    request("/documents", { method: "POST", body: { title, content } }),
  updateDocument: (id, patch) =>
    request(`/documents/${id}`, { method: "PATCH", body: patch }),
  deleteDocument: (id) => request(`/documents/${id}`, { method: "DELETE" }),

  uploadDocument: (file) => {
    const fd = new FormData();
    fd.append("file", file);
    return request("/documents/upload", { method: "POST", body: fd, isForm: true });
  },

  addShare: (id, email, permission) =>
    request(`/documents/${id}/shares`, { method: "POST", body: { email, permission } }),
  removeShare: (id, userId) =>
    request(`/documents/${id}/shares/${userId}`, { method: "DELETE" }),
};

export { ApiError };
