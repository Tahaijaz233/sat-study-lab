import os
import subprocess
import sys

def setup():
    try:
        import fastapi
        import uvicorn
        import jinja2
        import pydantic
        import pypdf
        import httpx
    except ImportError:
        print("[SAT Study Lab] Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    from app.database import init_db
    from seed_data import seed_all
    init_db()
    seed_all()

if __name__ == "__main__":
    setup()
    import uvicorn
    print("\n=======================================================")
    print(" SAT Study Lab is running on http://localhost:8000")
    print("=======================================================\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
