import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In dev, the SPA runs on :5173 and proxies /api to the FastAPI server on :8000,
// so the frontend code always calls same-origin "/api/..." paths. In production
// the same code works because FastAPI serves both the API and the built SPA.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: process.env.VITE_API_PROXY || "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: "dist",
  },
});
