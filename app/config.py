import os

class Config:
    # Use DATABASE_URL env var for PostgreSQL (Railway + Neon)
    # Falls back to SQLite file path for local development
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{os.getenv('DB_PATH', 'sat_lab.db')}")
    APP_NAME = "SAT Study Lab"

config = Config()
