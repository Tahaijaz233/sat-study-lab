import os

# Vercel serverless functions run from a read-only filesystem; only /tmp is
# writable. SQLite therefore uses /tmp in serverless environments. Deployments
# that define DATABASE_URL use persistent PostgreSQL instead.
IS_SERVERLESS = bool(os.environ.get("VERCEL")) or bool(
    os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
)


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
    DB_PATH = os.getenv("DB_PATH", "/tmp/sat_lab.db" if IS_SERVERLESS else "sat_lab.db")
    APP_NAME = "SAT Study Lab"


config = Config()
