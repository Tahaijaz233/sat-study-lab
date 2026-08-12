"""
Vercel serverless entrypoint for SAT Study Lab.

Vercel's Python runtime natively supports ASGI, so this file mirrors the
official FastAPI-on-Vercel pattern: the FastAPI instance named ``app`` in
``app/main.py`` is exported here for discovery.

Note: Vercel resolves exactly one Python entrypoint per project and its
candidate search checks ``app/main.py`` before ``api/index.py``, so this shim
does not create a second serverless function — it just makes the entrypoint
explicit and keeps the ``api/`` layout used by Vercel's FastAPI starter.
"""

from app.main import app as app  # noqa: F401  (re-export for Vercel)
