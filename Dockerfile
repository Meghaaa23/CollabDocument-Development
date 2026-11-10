# Single-image build: compiles the React SPA, then serves it together with the
# FastAPI JSON API from one Python process. Deploy this anywhere that runs a
# container (Render, Railway, Fly.io, Cloud Run, etc.).

# ---- stage 1: build the frontend ----
FROM node:20-alpine AS frontend
WORKDIR /fe
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---- stage 2: backend + built SPA ----
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install -r backend/requirements.txt

COPY backend/ ./backend/
# Drop the Vite output where FastAPI expects it (backend/static).
COPY --from=frontend /fe/dist ./backend/static

WORKDIR /app/backend
EXPOSE 8000
# Shell form so ${PORT} (set by most hosts) is expanded at runtime.
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
