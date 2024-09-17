from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from API import run_fastapi_app
from FaceRec.app.main import run_flask

# Multithreading used to start both FastAPI and Flask apps at the same time.
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_flask)
        executor.submit(run_fastapi_app)
