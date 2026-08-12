"""
Vercel Serverless Function Handler for SAT Study Lab
=====================================================================
This file adapts the FastAPI application to run as a Vercel serverless
function using Mangum (AWS Lambda adapter for ASGI apps).

Vercel will automatically detect this file and route all requests to it.
"""

import os
import sys

# Add the project root to the path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from app.main import app

# Create the Mangum handler for Vercel/Lambda
# Mangum adapts ASGI apps (FastAPI) to run in serverless environments
handler = Mangum(app, lifespan="auto")

# Vercel expects a callable named 'handler' or we can use the newer format
# Also expose a direct app for local testing if needed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
