"""Application configuration.

All settings are read from environment variables so the same image runs in
local dev and in production. Sensible defaults keep local dev zero-config.
"""
import os


class Settings:
    # Where the SQLite file lives. On a host with a persistent disk (e.g. Render),
    # point this at the mounted volume, e.g. sqlite:////data/collabdocs.db
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./collabdocs.db")

    # Secret used to sign JWTs. MUST be overridden in production.
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))  # 24h

    # Comma-separated list of allowed CORS origins for the SPA during local dev.
    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")

    # Upload limits.
    MAX_UPLOAD_BYTES: int = int(os.getenv("MAX_UPLOAD_BYTES", str(5 * 1024 * 1024)))  # 5 MB

    # Default password for seeded demo accounts.
    DEMO_PASSWORD: str = os.getenv("DEMO_PASSWORD", "demo1234")


settings = Settings()
