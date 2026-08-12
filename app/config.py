import os

# Vercel serverless functions run from a read-only filesystem; only /tmp is
# writable. Detect that environment so SQLite lands in /tmp instead of trying
# to create "sat_lab.db" next to the code (which crashes with
# FUNCTION_INVOCATION_FAILED). Locally we keep the normal relative path.
IS_SERVERLESS = bool(os.environ.get("VERCEL")) or bool(
    os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
)


class Config:
    DB_PATH = os.getenv("DB_PATH", "/tmp/sat_lab.db" if IS_SERVERLESS else "sat_lab.db")
    APP_NAME = "SAT Study Lab"

config = Config()
